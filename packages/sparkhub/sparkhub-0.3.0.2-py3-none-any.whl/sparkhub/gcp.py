import argparse
import subprocess

def list_configurations():
    """
    Lists all the available configurations.

    Examples
    --------
    >>> list_configurations()
    NAME          IS_ACTIVE  ACCOUNT               PROJECT      COMPUTE_DEFAULT_ZONE  COMPUTE_DEFAULT_REGION
    my-config     True       my-account@gmail.com  my-project   us-central1-a         us-central1
    another-config False      my-account@gmail.com  another-proj us-west1-a            us-west1
    """
    subprocess.run(["gcloud", "config", "configurations", "list"], check=True)

def activate_and_reset_config(config):
    """
    Activates the specified configuration and resets the application-default credentials.

    Parameters
    ----------
    config : str
        The name of the configuration to activate.

    Examples
    --------
    >>> activate_and_reset_config("my-config")
    Activating configuration: my-config
    Revoking application-default credentials...
    Acquiring new user credentials...
    Credentials saved to [~/.config/gcloud/application_default_credentials.json]

    """
    subprocess.run(["gcloud", "config", "configurations", "activate", config], check=True)
    print(f"Activating configuration: {config}")
    
    subprocess.run(["gcloud", "auth", "application-default", "revoke"], check=True)
    print("Revoking application-default credentials...")
    
    subprocess.run(["gcloud", "auth", "application-default", "login"], check=True)
    print("Acquiring new user credentials...")

def main():
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(description="Google Cloud Platform command-line tool")
    parser.add_argument("-l", "--list-configurations", action="store_true", help="List all available configurations")
    parser.add_argument("-c", "--activate-config", type=str, help="Activate and reset the specified configuration")
    args = parser.parse_args()

    if args.list_configurations:
        list_configurations()
    elif args.activate_config:
        activate_and_reset_config(args.activate_config)
    else:
        parser.print_help()