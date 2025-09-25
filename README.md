# scraper-api
🚀 Flask Scraper Setup & Usage with Make.com
1. Start Flask API (First Command Prompt)

Open Command Prompt.

Run the following commands:

cd Desktop
cd Scraper-Api
venv\Scripts\activate.bat
py scraper.py


This will start the Flask app locally at:
👉 http://127.0.0.1:3001

2. Expose API with Ngrok (Second Command Prompt)

Open another Command Prompt.

Run:

C:\Users\lenovo\Downloads\ngrok-v3-stable-windows-amd64\ngrok.exe http 3001


Ngrok will generate a public forwarding link, e.g.:
👉 https://unexponible-denyse-unrestrainable.ngrok-free.dev

3. Use in Make.com

Copy the Ngrok public URL and paste it into the HTTP module URL in Make.com.

Before pasting job URLs into Google Sheets → deactivate the scenario in Make.com.

Paste all URLs into the sheet.

Reactivate the scenario → duplicates are automatically removed (via App Script), and the flow will run automatically.

🔹 Note

If we host this API permanently (on a server or cloud service), we won’t need Ngrok or multiple steps.
You’ll just paste the hosted API URL in Make.com, and from your side, you only need to add job URLs → results will come automatically. ✅
