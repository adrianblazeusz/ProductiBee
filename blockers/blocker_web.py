from func.json_manager import JSONManager


class Web_blocker:

    def __init__(self):
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.redirect = "127.0.0.1"
        self.site_to_kill = set()
        self.common_subdomains = {
            "facebook.com": ["en-us", "pl-pl", "es-la", "fr-fr", "de-de", "it-it", "ar-ar", "pt-br"]
        }

    def is_website_blocked(self, website):
        """
        Checks if a website is already blocked in the hosts file.
        """
        with open(self.hosts_path, "r") as file:
            content = file.read()
            return website in content

    def block_websites(self):
        """
        Block the websites by adding them to the hosts file.
        """
        with open(self.hosts_path, "r+") as file:
            content = file.read()
            for site in self.site_to_kill:
                www_site = "www." + site

                # Block the main domain and www variant
                if site not in content:
                    file.write(self.redirect + " " + site + "\n")
                if www_site not in content:
                    file.write(self.redirect + " " + www_site + "\n")
                
                # Block common subdomains if they exist in our dictionary
                subdomains = self.common_subdomains.get(site, [])
                for subdomain in subdomains:
                    full_subdomain = subdomain + "." + site
                    if full_subdomain not in content:
                        file.write(self.redirect + " " + full_subdomain + "\n")

    def unblock_websites(self):
        """
        Unblock the websites by removing them from the hosts file.
        """
        with open(self.hosts_path, "r") as file:
            lines = file.readlines()
        
        with open(self.hosts_path, "w") as file:
            for line in lines:
                if not any(site in line for site in self.site_to_kill):
                    file.write(line)

    def set_blocked_websites(self, websites_list):
        for website in websites_list:
            if "www." in website:
                self.site_to_kill.add(website.replace("www.", ""))
            else:
                self.site_to_kill.add(website)

if __name__ == "__main__":

    web = Web_blocker()
    web.block_websites()
    print(web.site_to_kill)