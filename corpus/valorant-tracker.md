# valorant-tracker

# Valorant Tracker (HenrikDev API)

Small-scale personal project: a few friends link their Riot ID, get a dashboard
in the app, and a home screen widget showing rank + last match.

## 1. Get a HenrikDev API key

1. Join their Discord (linked from https://github.com/Henrik-3/unofficial-valorant-api)
2. Generate a key at https://api.henrikdev.xyz/dashboard/
3. Describe your use case honestly when asked ("personal stats app for me and a
   few friends") — this is exactly the kind of use they built the free tier for.

## 2. Backend setup (same droplet as Pratify)

```bash
cd backend
npm install
cp .env.example .env
# edit .env and paste in your HenrikDev key
npm start          # sanity check locally first

# on the droplet, run it under pm2 like Pratify's express server:
pm2 start server.js --name valorant-backend
pm2 save
```

Open the port you chose (default 3001) in your droplet's firewall/ufw if it's
not already open.

**Field names to double check:** the HenrikDev response shapes for `/v3/mmr`
and `/v4/matches` are assumed in `server.js` based on their docs
(https://docs.henrikdev.xyz) — once you have a real key, hit the endpoints and
`console.log(JSON.stringify(data, null, 2))` once to confirm the actual field
paths match (`stats.kills`, `agent.name`, etc.) before trusting the dashboard
output. HenrikDev has renamed a few fields between API versions before.

## 3. Mobile app setup

```bash
npx create-expo-app valorant-tracker-mobile
cd valorant-tracker-mobile

# delete the generated App.js and app.json, then copy in this project's:
#   app.config.js, App.js, src/

npx expo install react-native-android-widget @react-native-async-storage/async-storage expo-constants
```

Set your backend URL either in `app.config.js` directly or via an env var:

```bash
export BACKEND_URL="http://YOUR_DROPLET_IP:3001"
```

### Widget won't run in Expo Go

`react-native-android-widget` needs native code, same situation as `expo-av`
was for Pratify. You need a custom dev client:

```bash
eas build --profile development --platform android
```

Install the resulting APK on your (and your friends') phones, then run:

```bash
npx expo start --dev-client
```

For a real release later (not just dev testing), build a normal APK/AAB with
`eas build --platform android` once everything's confirmed working.

### Adding the widget to the home screen

Long-press on the home screen → Widgets → "Valorant Tracker" → drag it on.
It'll show placeholder text until you open the app once and link an account —
opening the app force-pushes fresh data to the widget immediately.

Android enforces a practical floor of ~15–30 min on background widget
refreshes regardless of `updatePeriodMillis` (battery optimization), so treat
the periodic refresh as "eventually consistent" — opening the app is what
gives you an instant update.

## 4. Sharing with friends

Each friend installs the same dev-client build (or eventually a release APK),
opens the app, and links **their own** Riot ID — no login/OAuth needed since
HenrikDev doesn't require RSO. Everyone points at the same backend URL; the
in-memory cache in `server.js` keeps you well under HenrikDev's rate limit
for a handful of users.

If this ever grows past "me and a few friends," the two things to revisit
first are: (1) swap the in-memory cache for something persistent (SQLite/Redis)
so it survives restarts, and (2) put the backend behind HTTPS (nginx +
certbot) and drop `usesCleartextTraffic` from `app.config.js`.
