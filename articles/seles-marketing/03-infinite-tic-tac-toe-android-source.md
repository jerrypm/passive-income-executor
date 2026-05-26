<!--
PLATFORM: Medium
POST DATE: 2026-05-30 (4 days after post 1)
PRODUCT: Infinite Tic-Tac-Toe Android App — Complete Kotlin Source Code with AdMob
ORIGINAL: $14 → FLASH: $4.9 (65% OFF)
GUMROAD: https://zerix1.gumroad.com/l/pheupx
TAGS: Android Development, Kotlin, Indie Game Dev, Mobile Development, Side Projects
SUGGESTED TITLE: I Built a Tic-Tac-Toe Game with a "Forever Mode" — and Earned My First $63 on AdMob. Here's the Whole Source.
SUBTITLE: One weekend, one Kotlin project, one stupidly addictive twist on a 5,000-year-old game. The full code is $4.90 this week.
-->

# I Built a Tic-Tac-Toe Game with a "Forever Mode" — and Earned My First $63 on AdMob. Here's the Whole Source.

### One weekend, one Kotlin project, one stupidly addictive twist on a 5,000-year-old game. The full code is $4.90 this week.

---

Most indie devs I know are stuck in the same loop.

They open Android Studio. They start a new project. They sketch something ambitious — a roguelike, a puzzle MMO, a "Wordle but multiplayer" thing. Three weeks in, the scope balloons. The motivation dies. The repo joins the graveyard of 47 abandoned folders in `~/AndroidStudioProjects`.

Sound familiar?

Here's the trick I learned the hard way: **the apps that actually ship — and actually make money — are the dumbest, smallest ideas you can think of.**

Mine was tic-tac-toe.

Yes, tic-tac-toe. The game your grandmother taught you on a paper napkin.

The twist: instead of resetting after every win, the board *keeps going*. Only your 3 most recent X's count. Place a 4th, the oldest one disappears. Suddenly a "solved" game has infinite replayability and a real strategic layer.

I shipped it in 9 days. AdMob banner + interstitial + rewarded ad on hint button. First $63 came in two months later.

Not life-changing. But it taught me everything that schools and YouTube tutorials don't.

---

## Why this specific build is worth studying

I'm not the first person to make tic-tac-toe in Kotlin. Probably not the 1,000th either.

But almost every Kotlin tutorial out there teaches you tic-tac-toe at the *introductory* level — a single Activity, manual View bindings, a 2D array, win-check function. Cool for hour 1.

What's missing in those tutorials is the entire **"actually-ship-this" layer**:

- AdMob integration that doesn't get your account banned (banner, interstitial, rewarded — all three)
- Proper consent dialog (UMP SDK) for EU users — required, ignored by 80% of indie devs
- A clean game state architecture using ViewModel + StateFlow (no spaghetti)
- Settings persistence with DataStore (not SharedPreferences, which Google now flags as legacy)
- Sound effects with proper pooling (so the audio doesn't lag on cheap devices)
- Light/dark theme that actually responds to system setting
- A "rate this app" prompt that fires at the *right* psychological moment (after the 3rd win)
- Play Store-ready assets folder (icon variants, feature graphic spec, screenshot templates)

That's the difference between "a tic-tac-toe app" and "a tic-tac-toe app that can survive Play Store and monetize."

---

## Who this is actually for

I'm going to be specific because vague pitches waste everyone's time.

**You're a good fit if:**
- You're learning Kotlin and you want a real, complete, *shipping-quality* codebase to read instead of another 90-minute YouTube tutorial.
- You're an experienced dev from another platform (iOS, web) and you want to learn the *Android way* of structuring an app — without sitting through 12 hours of Udemy.
- You're an indie publisher who wants a fast, polished base to reskin for your own theme (sci-fi tic-tac-toe? dinosaurs? emoji?). Reskin → relaunch in a weekend.
- You want to study how AdMob is *correctly* integrated end-to-end, including UMP consent, ad loading timing, and rewarded ad patterns — because the official docs are scattered across 19 pages.

**You're a bad fit if:**
- You want to copy-paste, push to Play Store with no changes, and expect free money. The Store algorithm will eat you alive. (Reskin matters.)
- You think Kotlin is a Russian dance.

---

## What's inside the package

When you grab it, you get:

```
infinite-tic-tac-toe/
├── app/
│   ├── src/main/
│   │   ├── java/com/jrdevhub/infinitetictactoe/
│   │   │   ├── ui/            (Compose screens + theme)
│   │   │   ├── game/          (state, win-check, infinite-mode logic)
│   │   │   ├── ads/           (AdMob wrapper, UMP consent)
│   │   │   ├── data/          (DataStore, settings repo)
│   │   │   └── sound/         (pooled SoundPool wrapper)
│   │   ├── res/               (drawables, strings-id + strings-en)
│   │   └── AndroidManifest.xml
│   └── build.gradle.kts       (latest stable: AGP, Kotlin, Compose BOM)
├── README.md                  (setup, build, reskin, ship — step by step)
├── PLAY_STORE_ASSETS/         (icon templates, feature graphic, screenshot frames)
└── ADMOB_SETUP.md             (your test IDs, where to swap real IDs, payout)
```

Built with:
- **Kotlin 2.0+** & **Jetpack Compose**
- **Android Gradle Plugin** (latest stable, May 2026)
- **AdMob SDK** + **UMP Consent SDK**
- **DataStore** (replaces SharedPreferences)
- **ViewModel + StateFlow** (no RxJava bloat)
- **Min SDK 24, Target SDK 34** (Play Store-current)

License: **personal use + 1 commercial release**. (Reskin and ship one game from it. Want to ship multiple? Email me, separate license.)

---

## Why I'm dropping it to $4.90 this week

The source code is normally $14. That's already cheap — CodeCanyon equivalents run $30-80 for less.

But this isn't really about the price. It's about who gets to study it.

There are devs in Indonesia, Pakistan, Nigeria, Brazil — where $14 is a meaningful spend — who would learn 10x more from reading a *complete, shipping codebase* than from another tutorial. I want them to have it.

So **this week — May 30 to June 6, 2026** — it's $4.90.

The price of a Big Mac. One sit-down at a warung. Half a Starbucks.

If even *one* pattern in the code — the consent flow, the rewarded ad timing, the StateFlow architecture — saves you a week of head-scratching, you've made the price back 50x in hourly value.

[**→ Grab Infinite Tic-Tac-Toe Source for $4.90 (until June 6)**](https://zerix1.gumroad.com/l/pheupx)

After June 6, back to $14.

---

## The bigger lesson

Honestly, the game itself isn't the point.

The point is: **stop trying to build the next Clash of Clans on your weekends.** Build a tic-tac-toe with one weird twist. Ship it. Watch it earn $63. Reskin it. Ship the reskin. Earn another $63.

Six reskins later you've shipped more apps than 99% of devs who "have a great idea." And you've learned, in your bones, every piece of the Play Store lifecycle.

That's the real product I'm selling. The code is just the proof.

[**Get the source for $4.90 →**](https://zerix1.gumroad.com/l/pheupx)

---

*Building something? Drop a screenshot in the comments — I love seeing what other indies are shipping. If this post helped you start, a clap pays it forward.*
