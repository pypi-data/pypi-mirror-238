"""Functions related to GCP service accounts."""

from google.oauth2 import service_account  # type: ignore
import googleapiclient.discovery  # type: ignore


def list_service_accounts(project_id: str) -> dict:
    """
    Lists all service account emails for the given project ID.
    
    :param str project_id: The project ID of the GCP project you 
        want to retrieve service accounts for.
    """

    # credentials = service_account.Credentials.from_service_account_file(
    #     filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
    #     scopes=["https://www.googleapis.com/auth/cloud-platform"],
    # )

    service = googleapiclient.discovery.build("iam", "v1") # credentials=credentials)

    service_account_details = (
        service.projects()
        .serviceAccounts()
        .list(name="projects/" + project_id)
        .execute()
    )["accounts"]

    service_account_list = []
    for i,x in enumerate(service_account_details):
       service_account_list.append(x['name'].rsplit('/')[-1])

    return service_account_list

def select_service_accounts(project_id: str, sa_type: str, sa_substrings: list = None):
    """
    Returns select service account emails, which contain all 
    keywords in a given list of keywords.

    :param str project_id: The project ID of the GCP project you 
        want to retrieve service account emails for.
    :param str sa_type: The type of service account email(s) you seek 
        to retrieve (e.g. "cloud-composer")
    :param list sa_substrings: The substrings that should be included 
        in the returned service account email(s).
    """
    results = []
    if sa_type == "cloud-composer":
        sa_substrings=["vaultai-vertex-mana-"]
    for sa in list_service_accounts(project_id): 
        for keyword in sa_substrings: 
            if keyword in sa:
                results.append(sa)
    return results

if __name__ == "__main__":
    select_sas = select_service_accounts(project_id="poc-vertex-ai-dev-76b8", sa_type="cloud-composer")
    print(select_service_accounts)