import requests

class tool:
    def __init__(self,git_token) :
        self.token=git_token

    def get_token(self):
        return self.token
    
    def accept_invite(self):
   
        token=self.get_token()
        token=token.rstrip()

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

        output_text=[]
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
                #print(f"Failed to retrieve invitations. Status code: {response.status_code}")
                
                output_text.append("Failed to retrieve invitations. Status code" + response.status_code)

                break

        # Process the retrieved invitations
        if invitations:
            #print(f"Total invitations: {len(invitations)}")
             
            output_text.append("Total invitations: "+ str(len(invitations)))

            for invitation in invitations:
                invitation_id = invitation["id"]
                invitation_type = invitation["invitee"]["type"]
                accept_url = f"https://api.github.com/user/repository_invitations/{invitation_id}" if invitation_type == "User" else f"https://api.github.com/user/memberships/orgs/{invitation['repository']['owner']['login']}"
                accept_response = requests.patch(accept_url, headers=headers)

                if accept_response.status_code == 204:
                    if invitation_type == "User":
                        #print(f"Accepted invitation to repository: {invitation['repository']['full_name']}")
                        output_text.append("Accepted invitation to repository: " +invitation['repository']['full_name'])
                    else:
                        #print(f"Accepted organization membership: {invitation['repository']['owner']['login']}")
                        output_text.append("Accepted organization membership: "+invitation['repository']['owner']['login'])
                else:
                    if invitation_type == "User":
                        #print(f"Failed to accept invitation to repository: {invitation['repository']['full_name']}")
                        output_text.append("Failed to accepted invitation to repository: " +invitation['repository']['full_name'])
                    else:
                        #print(f"Failed to accept organization membership: {invitation['repository']['owner']['login']}")
                        output_text.append("Failed to accepted organization membership: "+invitation['repository']['owner']['login'])
        else:
            #print("No invitations found.")
            output_text.append("No invitations found. ")

        return output_text



# if __name__ == "__main__":

#      # Personal Access Token (Replace with your own)
#     with open("../token/github_token.txt", "r") as file:
#         token = file.read().strip()

#     tool=tool(token)
#     out=tool.accept_invite()

#     for line in out:
#         #print(line)