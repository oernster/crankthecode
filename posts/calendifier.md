---
title: "Calendifier"
date: "2026-01-19 06:35"
tags: ["calendar", "event", "events", "RFC5545", "notes", "internationalization", "clock"]
blurb: "Calendar tool"
one_liner: "A calendar app with full iCalendar (RFC5545) support and deep internationalisation across languages and locales."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/calendifier.png
extra_images:
  - /static/images/calendifier-ha.png
---
# 📅 Calendifier

# Challenges along the way
The main app was HARD due to internationalization; this was my first foray into internationalizing an app and I did it 
for BOTH a browser AND home assistant dashboard cards.
Another really difficult thing for me was not only identifying holidays for locales which aren't British but making them 
appear correctly on the UI depending on the locale selected.
However, aside from the aforementioned internationalization support challenges, I really struggled through writing code to support
RFC5545 which is basically the official canonical way to support Eventing in a Calendar application.  I got there in the end though
and I feel the UI is relatively intuitive for this purpose.

## 🌟 Overview

**Calendifier** is a sophisticated calendar system available in two deployment modes:

1. **🖥️ Desktop Application** - Cross-platform desktop calendar built with Python and PySide6
2. **🏠 Home Assistant Integration** - Web-based dashboard cards for Home Assistant with beautiful UI

Both versions feature comprehensive internationalization supporting **40 languages** and **40 countries**, making it a truly global calendar solution.
One huge takeaway I had from this piece of work was that internationalization is an incredibly HARD thing to implement!

### ✨ Key Features

- 📅 **Full Calendar Management** - Monthly view with intuitive navigation
- 🌍 **40-Language Support** - Complete localization with runtime language switching
- 🏳️ **40-Country Holiday Support** - Intelligent holiday detection with native translations
- 🕐 **Real-time Analog Clock** - NTP synchronization for accurate timekeeping
- 📝 **Comprehensive Event Management** - Create, edit, delete with categories and recurring events
- 🎨 **Dynamic Theming** - Dark/Light mode with instant switching
- 📝 **Integrated Notes** - Built-in note-taking functionality
- 📤📥 **Import/Export** - Support for iCalendar, CSV, and JSON formats
- ⚙️ **Extensive Configuration** - Customizable settings for all preferences

## 🌍 International Support

### 🗣️ Supported Languages
- **🇺🇸🇬🇧 English** (US & UK variants)
- **🇨🇦 Français (Québec)** (Quebec French)
- **🇪🇸 Català** (Catalan)
- **🇪🇸 Español** (Spanish)
- **🇫🇷 Français** (French)
- **🇩🇪 Deutsch** (German)
- **🇮🇹 Italiano** (Italian)
- **🇧🇷 Português** (Brazilian Portuguese)
- **🇵🇹 Português** (Portuguese)
- **🇷🇺 Русский** (Russian)
- **🇨🇳 简体中文** (Simplified Chinese)
- **🇹🇼 繁體中文** (Traditional Chinese)
- **🇯🇵 日本語** (Japanese)
- **🇰🇷 한국어** (Korean)
- **🇮🇳 हिन्दी** (Hindi)
- **🇸🇦 العربية** (Arabic)
- **🇨🇿 Čeština** (Czech)
- **🇸🇪 Svenska** (Swedish)
- **🇳🇴 Norsk** (Norwegian)
- **🇩🇰 Dansk** (Danish)
- **🇫🇮 Suomi** (Finnish)
- **🇳🇱 Nederlands** (Dutch)
- **🇵🇱 Polski** (Polish)
- **🇹🇷 Türkçe** (Turkish)
- **🇺🇦 Українська** (Ukrainian)
- **🇬🇷 Ελληνικά** (Greek)
- **🇮🇩 Bahasa Indonesia** (Indonesian)
- **🇻🇳 Tiếng Việt** (Vietnamese)
- **🇹🇭 ไทย** (Thai)
- **🇧🇬 Български** (Bulgarian)
- **🇸🇰 Slovenčina** (Slovak)
- **🇸🇮 Slovenščina** (Slovenian)
- **🇭🇷 Hrvatski** (Croatian)
- **🇭🇺 Magyar** (Hungarian)
- **🇷🇴 Română** (Romanian)
- **🇮🇱 עברית** (Hebrew)
- **🇪🇪 Eesti** (Estonian)
- **🇱🇻 Latviešu** (Latvian)
- **🇱🇹 Lietuvių** (Lithuanian)

### 🏳️ Holiday Support
The application automatically detects and displays holidays for 40 countries with intelligent cultural filtering:

- 🇺🇸 United States | Federal holidays | ✅ 
- 🇨🇦 Canada | Jours fériés / Holidays | ✅ 
- 🇬🇧 United Kingdom | Bank holidays | ✅ 
- 🇪🇸 Spain | National holidays | ✅ 
- 🇫🇷 France | Jours fériés | ✅ 
- 🇩🇪 Germany | Feiertage | ✅ 
- 🇮🇹 Italy | Giorni festivi | ✅ 
- 🇧🇷 Brazil | Feriados nacionais | ✅ 
- 🇵🇹 Portugal | Feriados nacionais | ✅ 
- 🇷🇺 Russia | Праздничные дни | ✅ 
- 🇨🇳 China | 法定节假日 | ✅ 
- 🇹🇼 Taiwan | 國定假日 | ✅ 
- 🇯🇵 Japan | 祝日 | ✅ 
- 🇰🇷 South Korea | 공휴일 | ✅ 
- 🇮🇳 India | राष्ट्रीय अवकाश | ✅ 
- 🇸🇦 Saudi Arabia | الأعياد الوطنية | ✅ 
- 🇨🇿 Czech Republic | Státní svátky | ✅ 
- 🇸🇪 Sweden | Helgdagar | ✅ 
- 🇳🇴 Norway | Helligdager | ✅ 
- 🇩🇰 Denmark | Helligdage | ✅ 
- 🇫🇮 Finland | Juhlapäivät | ✅
- 🇳🇱 Netherlands | Feestdagen | ✅ 
- 🇵🇱 Poland | Święta państwowe | ✅ 
- 🇹🇷 Turkey | Resmi tatiller | ✅ 
- 🇺🇦 Ukraine | Державні свята | ✅ 
- 🇬🇷 Greece | Εθνικές γιορτές | ✅ 
- 🇮🇩 Indonesia | Hari libur nasional | ✅ 
- 🇻🇳 Vietnam | Ngày lễ quốc gia | ✅ 
- 🇹🇭 Thailand | วันหยุดราชการ | ✅ 
- 🇧🇬 Bulgaria | Национални празници | ✅ 
- 🇸🇰 Slovakia | Štátne sviatky | ✅ 
- 🇸🇮 Slovenia | Državni prazniki | ✅ 
- 🇭🇷 Croatia | Državni blagdani | ✅ 
- 🇭🇺 Hungary | Nemzeti ünnepek | ✅ 
- 🇷🇴 Romania | Sărbători naționale | ✅ 
- 🇮🇱 Israel | חגים לאומיים | ✅ 
- 🇪🇪 Estonia | Riigipühad | ✅ 
- 🇱🇻 Latvia | Valsts svētki | ✅ 
- 🇱🇹 Lithuania | Valstybės šventės | ✅ 

## ✨ Home Assistant Features
- 🎨 **Beautiful Dashboard Cards** - Clock, Calendar, Events, Notes, Settings, Data Management
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🌐 **Web Access** - Access from anywhere on your network
- 🔄 **Auto-Updates** - Cards refresh automatically
- 🎯 **Optimized Layout** - No overlapping, proper spacing

---

## 🖥️ Desktop Application

Traditional desktop application for local use.

### 🎯 First Launch

On first launch, the application will:
- 🔍 **Auto-detect your system locale** and set the appropriate language

- 🏳️ **Match your country** to display relevant holidays

- 🎨 **Apply your system theme** (dark/light mode)

- 📁 **Create user data directory** at `~/.calendar_app/`

### 🌙 Dark Theme

### ☀️ Light Theme

### 🌍 Language Switching

### 📝 Event Management

## 📦 Building & Distribution

Calendifier supports multiple build targets for maximum compatibility across platforms:

### 🖥️ Cross-Platform Executable (Nuitka)

Build a single executable file for Windows, macOS, and Linux:

## ⚙️ Configuration

### 🏠 User Data Location

The application stores user data in:
- **Windows:** `%USERPROFILE%\.calendar_app\`
- **macOS:** `~/.calendar_app/`
- **Linux:** `~/.calendar_app/`

### 📁 Configuration Files

- **`settings.json`** - Application preferences
- **`data/calendar.db`** - SQLite database
- **`logs/`** - Application logs
- **`exports/`** - Exported calendar files
- **`backups/`** - Database backups

**Made with ❤️ for the global community**

*Supporting 40 languages and 40 countries worldwide*
