from datetime import date, datetime, timedelta
import pytz
from .api_client import HubstuffApiClient
from .logger import get_root_logger


logger = get_root_logger(__name__)

utc = pytz.UTC


class HubstuffDataParser:
    api_client: HubstuffApiClient


    def __init__(self, api_client: HubstuffApiClient):
        self.api_client = api_client


    def get_organizations(self):
        '''Returns an array of organizations
        or raise an exception
        '''
        organizations = self.api_client.make_get_request('/company')
        return organizations


    def add_activity(self, activities_map: dict, user_id: int, project_id: int, duration: timedelta):
        # Chop microseconds
        duration = duration - timedelta(microseconds=duration.microseconds)
        if user_id in activities_map:
            if project_id in activities_map[user_id]:
                activities_map[user_id][project_id] += duration
            else:
                activities_map[user_id][project_id] = duration
        else:
            activities_map[user_id] = {project_id: duration}
        
    def get_activities_by_day(self, target_day: date):
        '''
        Returns a tuple of an object and a few dicts
        organization
        activities: [user_id][project_id] -> time_worked
        users: user_id -> user
        projects: project_id -> project
        '''
        start_time = datetime.combine(target_day, datetime.min.time())
        start_time = utc.localize(start_time)
        end_time = start_time + timedelta(days=1)
        organizations = self.get_organizations()
        if organizations is None or 'organizations' not in organizations:
            logger.error('Failed to get organizations')
            return None
        # Get only the 1st organization by default. Nothing was specified in the requirements in terms of which organization we should report
        organization = organizations['organizations'][0]
        if 'id' not in organization or 'name' not in organization:
            logger.error('Failed to get organization ID or name')
            return None
        organization_id = organization['id']
        logger.debug(f"Organization id={organization_id}, name={organization['name']}")
        start_time_iso = start_time.isoformat()
        end_time_iso = end_time.isoformat()

        activities_map: dict = {} # [user_id][product_id] -> duration
        prev_activity_map: dict = {} # [user_id][product_id] -> [starts_at, finished_at], Used for calculating overlaps between activities
        users_map = {}
        projects_map = {}

        page_start_id: int = 0
        page_size = 10
        while True:
            activities_response = self.api_client.make_get_request(
                f'/company/{organization_id}/work',
                headers_arg={'TimeSlotStart': start_time_iso, 'Include': 'users,projects', 'PageLimit': str(page_size)},
                params_arg={'time_slot[stop]': end_time_iso, 'page_start_id': page_start_id}
            )
            if activities_response is None or 'activities' not in activities_response or 'users' not in activities_response or 'projects' not in activities_response :
                return None
            activities = activities_response['activities']
            # Not sure activities are sorted, so sort them by ourselves by 'starts_at' field
            activities.sort(key=lambda activity: activity['starts_at'])
            users = activities_response['users']
            projects = activities_response['projects']
            for activity in activities:
                if ('user_id' not in activity) or (activity['user_id'] is None):
                    logger.warning(f"Failed to get user_id in activity {activity['id']}")
                    continue
                user_id = activity['user_id']

                if ('project_id' not in activity) or (activity['project_id'] is None):
                    logger.warning(f"Failed to get project_id in activity {activity['id']}")
                    continue
                project_id = activity['project_id']

                if ('starts_at' not in activity) or (activity['starts_at'] is None):
                    logger.warning(f"Failed to get starts_at in activity {activity['id']}")
                    continue
                starts_at = datetime.fromisoformat(activity['starts_at'])

                if ('updated_at' not in activity) or (activity['updated_at'] is None):
                    logger.warning(f"Failed to get updated_at in activity {activity['id']}")
                    continue
                finished_at = datetime.fromisoformat(activity['updated_at'])

                # Adjust starts_at, finished_at to the edge of the target day
                starts_at_fixed = starts_at if starts_at >= start_time else start_time
                finished_at_fixed = finished_at if finished_at <= end_time else end_time
                period = [starts_at_fixed, finished_at_fixed]
                if user_id in prev_activity_map:
                    if project_id in prev_activity_map[user_id]:
                        prev_period = prev_activity_map[user_id][project_id]
                        if prev_period[1] >= period[0]:
                            # If the end time of the previous activity is after the start time of the current activity, i.e. if the previous and current activities overlaps
                            prev_activity_map[user_id][project_id] = [prev_period[0], max(prev_period[1], period[1])]
                        else:
                            duration = prev_period[1] - prev_period[0]
                            self.add_activity(activities_map, user_id=user_id, project_id=project_id, duration=duration)
                            prev_activity_map[user_id][project_id] = period
                    else:
                        prev_activity_map[user_id][project_id] = period
                else:
                    prev_activity_map[user_id] = {project_id: period}
            
            for user in users:
                if user['id'] not in users_map:
                    users_map[user['id']] = user
            
            for project in projects:
                if project['id'] not in projects_map:
                    projects_map[project['id']] = project
            
            if 'pagination' not in activities_response or 'next_page_start_id' not in activities_response['pagination']:
                break
            page_start_id = activities_response['pagination']['next_page_start_id']

        # Add the final prev_activity
        for user_id, prev_activities_per_user in prev_activity_map.items():
            if prev_activities_per_user is None:
                continue
            for project_id, prev_activity in prev_activities_per_user.items():
                if prev_activity is None:
                    continue
                duration = prev_activity[1] - prev_activity[0]
                self.add_activity(activities_map, user_id=user_id, project_id=project_id, duration=duration)

        return organization, activities_map, users_map, projects_map