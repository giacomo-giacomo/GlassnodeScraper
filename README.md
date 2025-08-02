# Glassnode Scraper
Glassnode Data Scraper (Educational Purpose Only)
Disclaimer: This script is for educational purposes only. It is not intended to violate Glassnode’s Terms of Service.

### 📌 Overview
Web3 promotes transparency, openness, and public utility. Yet, accessing relevant on-chain data and metrics is often far from straightforward — even on platforms that claim to support these values.
This script demonstrates how to automate data extraction from Glassnode, particularly useful for retrieving recent on-chain metrics that require login access.

### 🔧 Features
-Logs into Glassnode using Selenium and saves session cookies
-Bypasses the 30-day data limitation for non-authenticated users
-Extracts on-chain metrics by sending requests to specific XHR endpoints
-Currently configured for Polygon metrics (modifiable)
