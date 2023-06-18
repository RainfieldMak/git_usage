import requests

# Personal Access Token (Replace with your own)
with open("github_token.txt", "r") as file:
    token = file.read().strip()

# GitHub API endpoint for retrieving invitations
invitations_url = "https://api.github.com/user/repository_invitations"

# Headers for the API request
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {token}",
    "User-Agent": "My-App"
}

invitations = []
page = 1

# Retrieve all invitations using pagination
while True:
    response = requests.get(f"{invitations_url}?page={page}", headers=headers)
    if response.status_code == 200:
        page_invitations = response.json()
        invitations.extend(page_invitations)
        if not page_invitations:
            break
        page += 1
    else:
        print(f"Failed to retrieve invitations. Status code: {response.status_code}")
        break

# Process the retrieved invitations
if invitations:
    print(f"Total invitations: {len(invitations)}")

    for invitation in invitations:
        invitation_id = invitation["id"]
        invitation_type = invitation["invitee"]["type"]
        accept_url = f"https://api.github.com/user/repository_invitations/{invitation_id}" if invitation_type == "User" else f"https://api.github.com/user/memberships/orgs/{invitation['repository']['owner']['login']}"
        accept_response = requests.patch(accept_url, headers=headers)

        if accept_response.status_code == 204:
            if invitation_type == "User":
                print(f"Accepted invitation to repository: {invitation['repository']['full_name']}")
            else:
                print(f"Accepted organization membership: {invitation['repository']['owner']['login']}")
        else:
            if invitation_type == "User":
                print(f"Failed to accept invitation to repository: {invitation['repository']['full_name']}")
            else:
                print(f"Failed to accept organization membership: {invitation['repository']['owner']['login']}")
else:
    print("No invitations found.")
