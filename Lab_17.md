# Lab 17 — Point-in-Time Audit

## Question

Was each number in **CPIAUCSL** knowable on the day it would have been used to make a Project 2 decision — and may Project 2 use it?

## Data card — CPIAUCSL

| Field | Record |
| --- | --- |
| Source | Federal Reserve Bank of St. Louis, [FRED series CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL); underlying producer: U.S. Bureau of Labor Statistics. |
| What it measures | Consumer Price Index for All Urban Consumers: All Items, seasonally adjusted; a broad measure of consumer-price inflation. |
| Units | Index, 1982–84 = 100; monthly, seasonally adjusted. |
| Publication lag | The value for a calendar month is released in the following month, usually around the middle of that month. For example, the September 2026 value was published on 14 October 2026, so it was not knowable on 30 September. |
| Revisions | The current values must not be assumed to be the vintage that was available historically. The ALFRED comparison is the control: it shows both release lag and any changed values on dates shared with today’s file. |
| Download date | 29 October 2026 (FRED/ALFRED public CSV downloads). |

### Three FRED-page spot checks

The current FRED download read: July 2026 **332.813**, August 2026 **334.131**, and September 2026 **336.298**. These are the three values I checked against the FRED series page.

### Point-in-time evidence

With the app set to **As known on 30 September 2026**, the latest CPIAUCSL observation is **August 2026, 334.131**. September’s 336.298 is absent because its release occurs after that decision date. On this particular comparison the app reported **0 revised shared dates**; that is evidence only for this vintage comparison, not permission to substitute today’s full history in a backtest.

## Partner attack — publication date

My partner trusted the publication date least. The app supplies the evidence: as of 30 September, the latest available CPI observation is August, although today’s file includes September; therefore a decision dated 30 September must not use September CPI.

## Your call

**Quarantine for raw Project 2 use; admit only through a point-in-time process.** CPIAUCSL is published after the measured month, so using today’s series at historical decision dates would leak future releases. I would admit it once each Project 2 decision date is paired with its ALFRED vintage (or an equivalent dated release record); a fixed, documented release-date rule would also need to be tested before use.

## Reflection

“Cleaned the data” is not a data card because it says nothing about the source, units, measurement date, publication date, or vintage. Those fields prevent a leak: an observation is eligible only if its release/vintage was available on the decision date, and units identify what the number actually represents. A backtest that uses today’s CPI values would make the strategy appear to know an inflation observation before its next-month release and could also incorporate later vintage changes.
