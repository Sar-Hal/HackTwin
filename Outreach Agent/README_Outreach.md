# 🚀 HackTwin Outreach Agent

An intelligent email outreach system that uses **Gemini AI** for personalized email generation, **SMTP** for email delivery, and **MongoDB** for data storage.

## 🔧 Features

- **AI-Powered Email Generation**: Uses Google's Gemini AI to create personalized emails
- **Email Delivery**: Sends emails via Gmail SMTP
- **Database Storage**: Stores user data and email status in MongoDB
- **Error Handling**: Comprehensive error handling and logging
- **Test Mode**: Generate and preview emails without sending them
- **Status Tracking**: Track email delivery status for each user

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **MongoDB Atlas Account** (free tier works)
3. **Google AI Studio Account** for Gemini API
4. **Gmail Account** with App Password enabled

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Update the `.env` file with your credentials:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Gemini AI Configuration  
GEMINI_API_KEY=your_gemini_api_key_here

# Email Configuration (Gmail SMTP)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

### 3. Gmail App Password Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings > Security > App Passwords
3. Generate a new App Password for "Mail"
4. Use this App Password (not your regular password) in `SENDER_PASSWORD`

### 4. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### 5. MongoDB Setup

1. Create a free MongoDB Atlas account
2. Create a new cluster
3. Get your connection string
4. Add it to your `.env` file as `MONGODB_URI`

## 🚀 Usage

### Running the Outreach Agent

```bash
python "Outreach Agent/agent.py"
```

**By default, the agent runs in TEST MODE** - it will generate emails without sending them.

### Test Mode vs Production Mode

**Test Mode (Default):**
- Generates personalized emails using AI
- Shows email previews in terminal
- Does NOT send actual emails
- Safe for testing and development

**Production Mode:**
- Actually sends emails via SMTP
- Updates user status in database
- Requires proper email credentials

To switch to production mode:
1. Configure `SENDER_EMAIL` and `SENDER_PASSWORD` in `.env`
2. Edit `agent.py` and comment out: `run_outreach(test_mode=True)`
3. Uncomment: `run_outreach(test_mode=False)`

### Managing Database

Use the database manager utility:

```bash
python db_manager.py
```

This utility allows you to:
- View all users in the database
- Reset user email statuses
- Add new users manually
- Export user data to JSON
- Delete all users (with confirmation)

## 📁 Project Structure

```
HackTwin/
├── Outreach Agent/
│   └── agent.py          # Main outreach agent script
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── db_manager.py        # Database management utility
└── README.md            # This file
```

## 🧪 Sample Data

The agent automatically creates 3 sample users when first run:

1. **Alice Johnson** - Machine Learning Engineer
2. **Bob Chen** - Full Stack Developer  
3. **Carol Williams** - Data Scientist

## 🔍 Email Template Structure

Each generated email includes:

1. **Personalized Greeting**: Uses recipient's name
2. **Introduction**: Brief intro to Hack-Nation hackathon
3. **Personalization**: Highlights recipient's relevant skills
4. **Call to Action**: Encourages participation
5. **Team Matchmaking**: Mentions AI-powered team matching
6. **Professional Closing**: Warm sign-off

## 📊 User Status Tracking

Users in MongoDB have the following statuses:
- `PENDING`: Ready to receive email
- `SENT`: Email successfully sent
- `ERROR`: Error occurred during sending

## ⚠️ Important Notes

1. **Rate Limiting**: Be mindful of Gmail's sending limits (500 emails/day for free accounts)
2. **Privacy**: Ensure compliance with email marketing laws (GDPR, CAN-SPAM)
3. **Testing**: Always test in TEST MODE before production use
4. **Security**: Never commit `.env` file with real credentials to version control

## 🐛 Troubleshooting

### Common Issues:

**"Authentication failed" Error:**
- Check if 2FA is enabled on Gmail
- Verify you're using App Password, not regular password
- Ensure `SENDER_EMAIL` and `SENDER_PASSWORD` are correct

**MongoDB Connection Error:**
- Verify `MONGODB_URI` is correct
- Check if your IP is whitelisted in MongoDB Atlas
- Ensure internet connection is stable

**Gemini API Error:**
- Verify `GEMINI_API_KEY` is valid
- Check if you've exceeded API quotas
- Ensure the API key has proper permissions

## 🆘 Support

If you encounter issues:

1. Check the terminal output for specific error messages
2. Verify all environment variables are set correctly
3. Test each component individually (MongoDB connection, Gemini API, SMTP)
4. Use the database manager to inspect user data

## 📈 Next Steps

To enhance the outreach agent:

1. **Add Email Templates**: Create multiple email templates for different campaigns
2. **Scheduling**: Add scheduled sending capabilities
3. **Analytics**: Track open rates and click-through rates
4. **Batch Processing**: Process users in batches for better performance
5. **Web Interface**: Create a web dashboard for managing campaigns

## 🔒 Security Best Practices

1. Keep your `.env` file secure and never commit it to version control
2. Use App Passwords instead of regular Gmail passwords
3. Regularly rotate API keys and passwords
4. Monitor your MongoDB access logs
5. Implement proper input validation for user data

---

**Happy Outreaching! 🚀**
