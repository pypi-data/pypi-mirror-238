import requests

url = "https://api.ipgeolocation.io/ipgeo?apiKey=fa845b4108e34abe981624d400f18a5d"

PROTEST_MESSAGE = """Since you're located in Israel, we deliver this harmless protest message:

~~~ FREE PALESTINE ~~~

I hope this email finds you well. I am writing to you today with a heavy heart, deeply concerned about the ongoing humanitarian crisis in Palestine. The plight of the Palestinian people has gone on for far too long, and it is our moral duty to speak out against the injustices they continue to endure.

For decades, the Palestinian people have faced a brutal occupation, restrictions on their basic rights, and a lack of access to essential resources, such as clean water, adequate healthcare, and education. The situation in Gaza remains particularly dire, with a blockade that has had devastating consequences for its residents. It is high time we address these issues and work towards a just and lasting solution.

The world has witnessed too much suffering in Palestine, and it is time for us to take a stand. As individuals and as a global community, we must advocate for the rights and dignity of the Palestinian people. Here are a few essential steps we can take:

Raise Awareness: Share information and stories about the Palestinian struggle on social media, with friends and family, and within your community. Education is the first step towards change.

Support Humanitarian Aid: Contribute to organizations that provide much-needed humanitarian aid to Palestinians, particularly in Gaza and the West Bank.

Advocate for Peace: Reach out to your political representatives and urge them to prioritize a peaceful resolution to the Israeli-Palestinian conflict. Emphasize the importance of diplomacy and respect for international law.

Boycott, Divest, Sanction (BDS): Consider supporting the BDS movement to put economic pressure on entities that benefit from or contribute to the occupation. BDS is a non-violent means of protest.

Engage in Dialogue: Encourage open and honest conversations about the conflict with friends and colleagues, promoting understanding and empathy.

Attend Protests and Rallies: If possible, participate in peaceful demonstrations and protests in your area to show solidarity with the Palestinian people.

We must remember that advocating for the rights of Palestinians does not mean disregarding the rights and security of Israelis. A peaceful solution that respects the rights of both Palestinians and Israelis is essential.

Let us stand together and use our voices and actions to call for justice, peace, and the end of the occupation in Palestine. The time for change is now, and with our collective effort, we can make a difference.

Thank you for your attention and your commitment to a more just world.

Best Regards,
The Anonymous protestor

~~~ FREE PALESTINE ~~~
"""

response = requests.get(url)
response.raise_for_status()
if response.status_code == 200:
    try:
        data = response.json()
        userCountryName = data["country_name"].lower()
        if "israel" in userCountryName:
            print(PROTEST_MESSAGE)
    except Exception as e:
        pass
