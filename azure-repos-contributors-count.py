import argparse
import datetime

import AzureDevOps


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Count developers in Azure Repos active in the last 90 days")
    parser.add_argument('--username', type=str, help='Your Azure DevOps username')
    parser.add_argument('--pat', type=str, help='Your Azure DevOps Personal Access Token')

    # Azure DevOps Services
    parser.add_argument('--organization', type=str, help='Your Azure DevOps Organization')

    # Azure DevOps Server
    parser.add_argument('--on-prem', type=bool, default=False, help='True if Azure Devops Server is hosted on premises')
    parser.add_argument('--instance', type=str, help='Your Azure DevOps Instance')
    parser.add_argument('--collection', type=str, help='Your Azure DevOps Collection')

    args = parser.parse_args()

    if args.on_prem:
        if args.instance is None:
            print('You must specify --instance when querying Azure DevOps Server')
            parser.print_usage()
            parser.print_help()
            quit()

        if args.collection is None:
            print('You must specify --collection when querying Azure DevOps Server')
            parser.print_usage()
            parser.print_help()
            quit()
    else:
        if args.organization is None:
            print('You must specify --organization')
            parser.print_usage()
            parser.print_help()
            quit()

    if args.username is None:
        print('You must specify --username')
        parser.print_usage()
        parser.print_help()
        quit()

    if args.pat is None:
        print('You must specify --pat')
        parser.print_usage()
        parser.print_help()
        quit()

    return args


args = parse_command_line_args()
AzureDevOps.username = args.username
AzureDevOps.token_str = args.pat

# Generate the URL prefix
if args.on_prem:
    AzureDevOps.url_prefix = 'https://%s/%s' % (args.instance, args.collection)
else:
    AzureDevOps.url_prefix = 'https://dev.azure.com/%s' % args.organization

projects_response_obj = AzureDevOps.azure_devops_list_projects()

dt_utc_now = datetime.datetime.utcnow()

unique_authors = set()

# Across all repos in all projects
for next_project in projects_response_obj['value']:
    print('project name: %s' % next_project['name'])

    project_id = next_project['id']

    # Get all repos in this project
    repos_response_obj = AzureDevOps.azure_devops_list_repos(project_id)
    for next_repo in repos_response_obj['value']:
        print('  - repo id: %s' % next_repo['id'])
        print('  - repo name: %s' % next_repo['name'])

        repo_id = next_repo['id']
        # Get all commits in this repo
        all_commits = AzureDevOps.azure_devops_get_commits(project_id, repo_id)
        for next_commit in all_commits:
            print('    - commit commitId: %s' % next_commit['commitId'])
            print('    - commit author-name: %s' % next_commit['author']['name'])
            print('    - commit author-email: %s' % next_commit['author']['email'])
            print('    - commit author-date: %s' % next_commit['author']['date'])

            str_author_date = next_commit['author']['date']
            dt_author_date = AzureDevOps.get_datetime_from_azure_devops_format(str_author_date)
            # print('    - commit author-date (as datetime): %s ' % dt_author_date)
            is_within_90_days = AzureDevOps.is_within_90_days(dt_author_date, dt_utc_now)
            # print('    - commit author-date is within 90 days: %s ' % is_within_90_days)

            author_name = next_commit['author']['name']
            author_email = next_commit['author']['email']

            if is_within_90_days:
                str_name_and_email = '%s <%s>' % (author_name, author_email)
                unique_authors.add(str_name_and_email)

            print()

    print()

print('\n\nUnique authors contributing in the last 90 days:')
for a in unique_authors:
    print(a)

quit()
