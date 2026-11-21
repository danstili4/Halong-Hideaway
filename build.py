"""Assemble the Halong Hideaway site: home, about, tours (+3 tour pages), gallery."""
from pathlib import Path

OUT = Path(__file__).parent / 'site'
IMG = 'https://halonghideaway.com/public/media/media/images/'
HOSTELS = 'https://www.centralbackpackershostel.com/'

TOURS = {
    2: dict(file='tour-2-days.html', name='2 days, 1 night', short='One night on the bay', price='3,150,000₫',
            book='https://halonghideaway.com/booking-tour/1751'),
    3: dict(file='tour-3-days.html', name='3 days, 2 nights', short='The full trip', price='4,900,000₫',
            book='https://halonghideaway.com/booking-tour/1741'),
    6: dict(file='tour-6-days.html', name='6 days with the Ha Giang Loop', short='The bay, then the mountains', price='from 8,800,000₫',
            book='https://halonghideaway.com/booking-tour/1752'),
}
PERDAY = {2: "Under 1.6 million ₫ a day", 3: "Under 1.7 million ₫ a day", 6: "Under 1.5 million ₫ a day"}
TOUR_FILES = {t['file'] for t in TOURS.values()} | {'tours.html'}


def img(file, alt, cls='shot feather', lazy=True):
    if file.startswith('g-'):  # Dan's own photos, stored with the site
        base = f'assets/media/gallery/{file}'
        return (f'<figure class="{cls}"><img src="{base}.jpg" srcset="{base}-sm.jpg 800w, {base}.jpg 1500w" '
                f'sizes="(max-width: 900px) 92vw, 45vw" alt="{alt}" loading="lazy" decoding="async"></figure>')
    lz = ' loading="lazy"' if lazy else ''
    oe = "this.parentNode.style.display='none'"
    return (f'<figure class="{cls}"><img src="{IMG}{file}" alt="{alt}"{lz} '
            f'referrerpolicy="no-referrer" onerror="{oe}"></figure>')


def nav(current):
    cur = ' aria-current="page"'
    def link(f, label):
        return f'<a href="{f}"{cur if f == current else ""}>{label}</a>'
    items = ''.join(
        f'\n        <a href="{t["file"]}"{cur if t["file"] == current else ""}><span><b>{t["name"]}</b><small>{t["short"]}</small></span></a>'
        for t in TOURS.values())
    dd_cls = 'dd current' if current in TOUR_FILES else 'dd'
    return f'''<nav id="menu" aria-label="Main">
    {link('index.html', 'Home')}
    {link('about.html', 'About us')}
    <div class="{dd_cls}">
      <button type="button" aria-expanded="false" aria-controls="tour-menu">Tours <svg viewBox="0 0 10 10" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
      <div class="dd-panel" id="tour-menu" hidden>{items}
        <a class="all" href="tours.html"{cur if current == 'tours.html' else ''}><span>Compare all tours</span></a>
      </div>
    </div>
    {link('gallery.html', 'Gallery')}
    <a href="{HOSTELS}" target="_blank" rel="noopener">Our hostels<span class="ext" aria-hidden="true">↗</span><span class="vh"> (opens in a new tab)</span></a>
    <a class="btn" href="tours.html">Book now</a>
  </nav>'''


FILM = '''<dialog id="film" aria-label="Halong Hideaway trip video">
  <button class="close" type="button">Close</button>
  <div class="frame"><iframe title="Halong Hideaway trip video" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
  <p class="film-note">Video not playing? <a class="film-out" href="#" target="_blank" rel="noopener">Watch it on YouTube</a></p>
</dialog>'''


def shell(file, title, desc, body, extra=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="world" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>

<header class="top">
  <a class="mark" href="index.html">Halong Hideaway</a>
  <div class="bar">
    <a class="btn bar-book" href="tours.html">Book now</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  {nav(file)}
</header>

<main id="main">
{body}
  <footer data-stop="evening">
    <p class="ask">Got a question? Just ask. <a href="tel:+84965651133">+84 965 651 133</a></p>
    <div>
      <ul>
        <li><a href="https://www.instagram.com/halonghideawaytour">Instagram</a></li>
        <li><a href="https://www.facebook.com/halonghideawaytour">Facebook</a></li>
        <li><a href="https://www.tripadvisor.com.vn/">TripAdvisor</a></li>
        <li><a href="https://www.youtube.com/watch?v=XsAsDFy_2qI">YouTube</a></li>
      </ul>
      <p class="fine">Run by <a href="{HOSTELS}" target="_blank" rel="noopener">Central Backpackers</a> and Buffalo Hostels, with hostels in Hanoi, Cat Ba, Ninh Binh, Phong Nha and Ha Giang. You don't need to stay with us to join.</p>
      <p class="fine">Tag your photos #halonghideaway</p>
      <p class="fine concept">Website concept by Dan.</p>
    </div>
  </footer>
</main>
{extra}
<script src="assets/site.js"></script>
</body>
</html>
'''


# ================================================================== HOME
home = f'''
  <section class="hero" data-stop="dawn">
    <div>
      <h1 class="display"><span>Come as strangers.</span><span class="heavy">Leave as friends.</span></h1>
      <p class="lede">Two or three days on Lan Ha Bay with a boatful of other backpackers. Swim off the deck, party at sunset, sleep on the water.</p>
      <div class="actions">
        <a class="btn" href="tours.html">Find my trip</a>
        <a class="more" href="tour-3-days.html">See the itinerary</a>
      </div>
      <ul class="trust"><li>Leaves Hanoi daily</li><li>Bed, meals and activities included</li><li>Run by Central Backpackers and Buffalo Hostels</li></ul>
    </div>
    <figure class="hero-shot hero-promo feather">
      <video class="loop" id="promo" src="assets/media/promo-preview.mp4" data-full="assets/media/promo.mp4" autoplay muted loop playsinline preload="auto" disablepictureinpicture disableremoteplayback
        poster="assets/media/promo-poster.jpg" aria-label="Halong Hideaway promo video: the boat, jumping in, banana tubing, the jacuzzi and the party"></video>
      <button class="play sound" type="button" aria-pressed="false"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M4 2.5v13l11-6.5z" fill="currentColor"/></svg><span>Watch with sound</span></button>
    </figure>
  </section>

  <section class="beat" data-stop="midday">
    <div>
      <h2 class="line">Jump off the boat. <b>Then do it again.</b></h2>
      <p class="lede">Backflips off the deck, banana tubing, volleyball on an empty beach. Then a jacuzzi to warm up.</p>
      <a class="more" href="tour-3-days.html">See the full trip</a>
    </div>
    <figure class="shot feather clip">
      <video class="loop" data-src="assets/media/jump-loop.mp4" muted loop playsinline preload="none" disablepictureinpicture disableremoteplayback
        poster="assets/media/jump-poster.jpg" aria-label="Guests jumping off the Hideaway boat into Lan Ha Bay"></video>
    </figure>
  </section>

  <section class="beat flip" data-stop="sunset">
    <div>
      <h2 class="line">Every night starts with <b>a sunset party.</b></h2>
      <p class="lede">Happy hour on the top deck as the sun drops behind the islands. BBQ, then the dance floor.</p>
    </div>
    <figure class="shot feather clip">
      <video class="loop" data-src="assets/media/sunset-loop.mp4" muted loop playsinline preload="none" disablepictureinpicture disableremoteplayback
        poster="assets/media/sunset-poster.jpg" aria-label="Two guests toasting with drinks on deck at sunset"></video>
    </figure>
  </section>

  <section class="beat" data-stop="night">
    <div>
      <h2 class="line">Coming alone? <b>Good.</b></h2>
      <p class="lede">Same boat, same beach, same party. By the last morning, you're paddling with people who'll be in your group chat for years.</p>
    </div>
    {img('g-beach-group', 'A big group of Hideaway guests on the beach next to the day boat')}
  </section>

  <section class="beat solo" data-stop="golden">
    <div>
      <h2 class="title">Bed, food and fun sorted. Bring swimwear.</h2>
      <ul class="facts">
        <li>Hostel pickup</li><li>Your cabin</li><li>All meals</li><li>Guide</li><li>Kayaks, tubing, volleyball</li><li>Free bag storage</li>
      </ul>
      <ul class="choose">
        <li><a href="tour-2-days.html"><span class="n">2 days, 1 night<small>One night, one sunset party, morning kayaks</small></span></a></li>
        <li><a href="tour-3-days.html"><span class="n">3 days, 2 nights<small>The full trip, plus cycling and trekking on Cat Ba</small></span></a></li>
        <li><a href="tour-6-days.html"><span class="n">6 days with the Ha Giang Loop<small>The cruise, then three days riding Ha Giang</small></span></a></li>
      </ul>
      <p class="note" style="margin-bottom:1.6rem">Drinks are on you. Everything else is covered.</p>
      <div class="actions">
        <a class="btn" href="tours.html">Book my spot</a>
        <a class="more" href="https://www.tripadvisor.com.vn/" target="_blank" rel="noopener">Read reviews on TripAdvisor</a>
      </div>
    </div>
  </section>
'''

# ================================================================== ABOUT
about = f'''
  <section class="intro" data-stop="dawn">
    <h1 class="display"><span>From the people</span><span class="heavy">behind your hostel.</span></h1>
    <p class="lede">Halong Hideaway is run by the team behind Central Backpackers and Buffalo Hostels. We built the trip we'd want to go on: a fair price, good food, good people and plenty to do.</p>
  </section>

  <section class="split" data-stop="midday" aria-labelledby="where">
    <div>
      <h2 class="title" id="where">The quiet side of the bay</h2>
      <p class="body" style="color:inherit">Halong Bay is beautiful, and busy. We skip the crowds and head for Lan Ha Bay and Cat Ba Island: calmer water, empty beaches and the view from the top of Cat Ba National Park.</p>
      <p class="body">Your guide fills you in on life on the bay along the way.</p>
    </div>
    {img('g-boat', 'The Hideaway Cruise anchored among the limestone islands of Lan Ha Bay')}
  </section>

  <section class="split flip" data-stop="midday" aria-labelledby="deck">
    <div>
      <h2 class="title" id="deck">The boat</h2>
      <p class="body" style="color:inherit">The Hideaway is a 5-star cruise that anchors overnight in the bay, away from the busy routes.</p>
      <ul class="spec">
        <li><b>3</b><span>Big shared jacuzzis. Most afternoons end in one.</span></li>
        <li><b>1</b><span>Sundeck for doing nothing between activities.</span></li>
        <li><b>1</b><span>Dance floor. You'll find it after the BBQ.</span></li>
      </ul>
    </div>
    {img('g-deck', 'Guests with drinks on the top deck at sunset, islands behind them')}
  </section>

  <section class="block" data-stop="sunset" aria-labelledby="eat">
    <h2 class="title" id="eat">Eating</h2>
    <p class="body" style="color:inherit;margin-top:1.4rem">Every meal is included and cooked fresh on board, with a BBQ on deck each night. Vegetarian or no seafood? Just tell us when you book.</p>
  </section>

  <section class="sleep" data-stop="dusk" aria-labelledby="sleep">
    <div class="sleep-copy">
      <h2 class="title" id="sleep">Sleeping</h2>
      <p class="body" style="color:inherit">After the party, head down to a wood-panelled cabin with proper beds, fresh linen and a kettle for the morning coffee.</p>
      <p class="body">The boat anchors out in the bay, so you fall asleep on the water and wake up to the islands.</p>
    </div>
    <div class="sleep-pics">
      <figure class="shot"><img src="assets/media/cabin-1.jpg" srcset="assets/media/cabin-1-800.jpg 800w, assets/media/cabin-1.jpg 1400w" sizes="(max-width: 900px) 50vw, 30vw" alt="A cabin on the Hideaway with carved wooden headboard, white linen and Hideaway Cruise cushions" loading="lazy" decoding="async"></figure>
      <figure class="shot"><img src="assets/media/cabin-2.jpg" srcset="assets/media/cabin-2-800.jpg 800w, assets/media/cabin-2.jpg 1400w" sizes="(max-width: 900px) 50vw, 30vw" alt="The same cabin seen from the doorway, with wood-panelled walls, a mirror and a kettle" loading="lazy" decoding="async"></figure>
    </div>
  </section>

  <section class="block" data-stop="mist" aria-labelledby="book-h">
    <h2 class="title" id="book-h">Booking with us</h2>
    <dl class="qa">
      <div><dt>Do I need to stay at your hostels?</dt><dd>No. Anyone can join. Book here or at the travel desk of any of our hostels.</dd></div>
      <div><dt>Where do tours start?</dt><dd>Every day, from Hanoi Central Backpackers or Hanoi Buffalo Hostel.</dd></div>
    </dl>
  </section>

  <section class="beat solo" data-stop="golden">
    <div>
      <h2 class="title">Pick your trip.</h2>
      <p class="lede">Two days, three days, or the bay plus the Ha Giang Loop.</p>
      <a class="btn" href="tours.html">Find my trip</a>
    </div>
  </section>
'''

# ================================================================== TOURS
def row(stop, n, t, title, hook, ticks, badge=''):
    tk = ''.join(f'<li>{x}</li>' for x in ticks)
    bd = f'<span class="badge">{badge}</span>' if badge else ''
    return f'''
  <section class="tour-row" data-stop="{stop}" aria-labelledby="t{n}">
    <p class="big" aria-hidden="true">{n}<small>{"days" if n > 1 else "day"}, {t["name"].split(", ")[1] if n != 6 else "6 nights"}</small></p>
    <div>
      {bd}
      <h2 id="t{n}">{title}</h2>
      <p class="hook">{hook}</p>
      <ul class="ticks">{tk}</ul>
    </div>
    <div class="buy">
      <p class="price">{t["price"].replace("from ", "")}<small>{"per person, riding yourself" if n == 6 else "per person, all meals included"}<span class="perday">{PERDAY[n]}</span></small></p>
      <a class="btn" href="{t["book"]}">Book my spot</a>
      <a class="more" href="{t["file"]}">See the full tour</a>
    </div>
  </section>'''


tours = f'''
  <section class="intro" data-stop="dawn" style="min-height:44vh">
    <h1 class="display"><span>Pick your</span><span class="heavy">trip.</span></h1>
    <p class="lede">All three leave Hanoi every day. Pickup, your cabin, meals and activities are included. Drinks are extra.</p>
    <ul class="trust"><li>Daily departures</li><li>Free bag storage at the hostel</li><li>Run by Central Backpackers and Buffalo Hostels</li></ul>
  </section>
{row('midday', 2, TOURS[2], 'Short on time? Do one night.',
     'The best bits in one night: the beach stop, the sunset party and morning kayaks.',
     ['Boat jumping, banana tubing, beach volleyball', 'Sunset happy hour, BBQ, party', 'Morning kayaking and a cooking demo', 'Back in Hanoi by 4:30pm'])}
{row('sunset', 3, TOURS[3], 'The full Hideaway.',
     'Two nights, two sunset parties and a day on Cat Ba Island. Most of our photos come from this one.',
     ['Everything in the 2-day trip, plus a second night', 'Cycling through Viet Hai village and a jungle trek', 'Lunch with a fish massage for tired feet', 'Sunset party, round two'], 'Our flagship trip')}
{row('mist', 6, TOURS[6], 'The bay, then the mountains.',
     'The full cruise, a night bus north, then three days riding the Ha Giang Loop.',
     ['The complete 3-day Hideaway cruise', 'Quan Ba pass, Ma Pi Leng pass and Dong Van', 'A boat trip on the Nho Que river', 'Homestays with local families'])}
'''

# ================================================================== TOUR PAGES
def head(n, l1, l2, lede):
    t = TOURS[n]
    small = ('per person, riding yourself. 9,800,000₫ with a driver.' if n == 6 else 'per person. Everything on the itinerary included.') + f'<span class="perday">{PERDAY[n]}</span>'
    return f'''
  <section class="tour-head" data-stop="dawn">
    <div>
      <h1 class="display"><span>{l1}</span><span class="heavy">{l2}</span></h1>
      <p class="lede">{lede}</p>
    </div>
    <div class="buy">
      <p class="price">{t["price"].replace("from ", "")}<small>{small}</small></p>
      <a class="btn" href="{t["book"]}">Book my spot</a>
      <p class="note">Leaving soon? Book now, then confirm at the hostel travel desk the day before.</p>
      <a class="more" href="#included">What's included</a>
    </div>
  </section>'''


DAY1 = f'''
    <section class="chapter" data-stop="midday" aria-labelledby="d1">
      <h2 id="d1"><small>Day one</small>Out of the city, into the bay</h2>
      <ol class="moments">
        <li><time>Morning</time><p>Pickup from Central Backpackers or Buffalo Hostel in Hanoi. Leave your big bag with us for free, then it's bus and boat out past Cat Ba National Park.</p></li>
        <li><time>Arrival</time><p>Lunch on board, then find your cabin.</p></li>
        <li><time>Afternoon</time><p>A smaller boat takes you to a quiet beach. <strong>Jump off the boat, ride the banana tube, play volleyball,</strong> or sit in the sand with a cold beer. Then back on board for the jacuzzis.</p></li>
      </ol>
      {img('g-backflip', 'A guest backflipping off the boat into the bay')}
    </section>

    <section class="chapter" data-stop="sunset" aria-label="Day one, evening">
      <p class="says">Happy hour starts when the sun goes down.</p>
      <ol class="moments">
        <li><time>Sunset</time><p>The boat heads to a quiet corner of the bay for the sunset party. Have your camera ready.</p></li>
      </ol>
    </section>

    <section class="chapter" data-stop="night" aria-label="Day one, night">
      <p class="says">Then the party.</p>
      <ol class="moments">
        <li><time>7:00</time><p>BBQ dinner on deck.</p></li>
        <li><time>Later</time><p>Dance floor, karaoke, beer pong, and a boat full of people you met this morning. Then you sleep on the water.</p></li>
      </ol>
      {img('g-dance', 'Guests dancing on the glowing dance floor', 'shot feather low')}
    </section>'''


def included(incl, excl, n):
    t = TOURS[n]
    li = ''.join(f'<li>{x}</li>' for x in incl)
    return f'''
  <section class="block" id="included" data-stop="golden" aria-labelledby="inc-h">
    <h2 class="title" id="inc-h">What's included</h2>
    <div class="cols">
      <div><h3>Included</h3><ul class="incl" style="margin:0">{li}</ul></div>
      <div><h3>Not included</h3><p class="body" style="margin-top:0">{excl}</p>
        <p class="price" style="font-size:clamp(2.2rem,4vw,3.2rem);margin-top:2rem">{t["price"].replace("from ", "")}<small>{"per person, riding yourself. 9,800,000₫ with a driver." if n == 6 else "per person"}</small></p>
        <p style="margin-top:1.4rem"><a class="btn" href="{t["book"]}">Book my spot</a></p>
      </div>
    </div>
  </section>'''


def before(n):
    shoes = ('<div><dt>Shoes</dt><dd>Proper trekking shoes for the Cat Ba jungle hike. Flip-flops won\'t cut it.</dd></div>' if n != 2 else
             '<div><dt>Shoes</dt><dd>Sandals are fine on the boat. Trainers if you want to explore at the beach stop.</dd></div>')
    hg = ('<div><dt>On the loop</dt><dd>Ride yourself or sit behind an experienced driver. Bike, fuel and guide are covered either way.</dd></div>' if n == 6 else '')
    return f'''
  <section class="block" data-stop="dusk" aria-labelledby="go-h">
    <h2 class="title" id="go-h">Before you go</h2>
    <dl class="qa">
      <div><dt>Where we meet</dt><dd>7:30am at Hanoi Central Backpackers or Hanoi Buffalo Hostel, every day. Your big bag stays at the hostel for free.</dd></div>
      <div><dt>What to pack</dt><dd>Passport, swimwear, sunscreen, insect repellent and a charged camera. Something warm from November to March.</dd></div>
      {shoes}
      {hg}
      <div><dt>Food</dt><dd>Vegetarian and no-seafood meals are easy. For stricter diets, tell us when you book; you may need to bring some of your own food.</dd></div>
      <div><dt>Confirm the day before</dt><dd>Stop by the travel desk the day before. Booking less than 24 hours out? Pay in full to hold your spot.</dd></div>
      <div><dt>If plans change</dt><dd>Cancel 30 days to 48 hours out and you pay 25% of the fare. 48 to 24 hours out, 50%. Inside 24 hours, the full fare.</dd></div>
    </dl>
  </section>'''


def others(n):
    links = ''.join(
        f'<a href="{t["file"]}"><b>{t["name"]}</b><span>{t["short"]}, {t["price"]}</span></a>'
        for k, t in TOURS.items() if k != n)
    return f'''
  <section class="block" data-stop="night" aria-labelledby="oth-h" style="padding-bottom:0">
    <h2 class="title" id="oth-h">Other tours</h2>
    <div class="others">{links}</div>
  </section>'''


def bookbar(n):
    t = TOURS[n]
    p = t['price'].replace('from ', '')
    return f'<a class="btn bookbar" href="{t["book"]}">Book for {p}</a>'


BASE_INCL = ['Bus and boat transfers from Hanoi', 'Tour guide', 'Entrance fees']
EXCL = 'Drinks, travel insurance and personal spending.'

tour2 = head(2, '2 days,', 'one night.', 'One night on the bay with the best bits: the beach stop, the sunset party and morning kayaks.') + f'''
  <div class="route" id="itinerary">{DAY1}

    <section class="chapter" data-stop="mist" aria-labelledby="d2">
      <h2 id="d2"><small>Day two</small>Quiet water</h2>
      <ol class="moments">
        <li><time>7:30</time><p>Breakfast in the boat's restaurant.</p></li>
        <li><time>8:30</time><p><strong>Guided kayaking</strong> around a quiet part of the bay, then back on board to shower and pack.</p></li>
        <li><time>9:45</time><p>Cooking demo on board.</p></li>
        <li><time>Or</time><p>Skip it all and stay in the jacuzzi.</p></li>
        <li><time>10:30</time><p>Lunch, then back to Hanoi.</p></li>
        <li><time>4:30</time><p>Back at the hostel.</p></li>
      </ol>
      {img('g-kayaks', 'Two kayaks paddling across turquoise water beneath a limestone cliff')}
    </section>
  </div>
''' + included(['One night in your cabin on the Hideaway', 'Lunch and dinner on day one, breakfast and lunch on day two'] + BASE_INCL[:1] + ['Kayaking, banana tubing, swimming and beach volleyball'] + BASE_INCL[1:], EXCL, 2) + before(2) + others(2)

tour3 = head(3, '3 days,', 'two nights.', 'The full Hideaway: two sunset parties, a day cycling and trekking Cat Ba Island, and kayaks on the last morning.') + f'''
  <div class="route" id="itinerary">{DAY1}

    <section class="chapter" data-stop="midday" aria-labelledby="d2">
      <h2 id="d2"><small>Day two</small>Cat Ba on two wheels and two feet</h2>
      <ol class="moments">
        <li><time>7:00</time><p>Breakfast in the boat's restaurant.</p></li>
        <li><time>9:00</time><p>Day boat to Cat Ba National Park, then <strong>cycle through Viet Hai village</strong>, past a tunnel and traditional houses.</p></li>
        <li><time>Trek</time><p>Up through the jungle to a view over the village and the bay. Proper shoes for this one.</p></li>
        <li><time>Lunch</time><p>At a local spot at the foot of the mountain, with a fish massage for tired feet.</p></li>
      </ol>
    </section>

    <section class="chapter" data-stop="dusk" aria-label="Day two, evening">
      <p class="says">Round two.</p>
      <ol class="moments">
        <li><time>Afternoon</time><p>Back on board for a jacuzzi, a beer and the sunset.</p></li>
        <li><time>7:00</time><p><strong>BBQ, then the party.</strong> By now everyone knows everyone.</p></li>
      </ol>
    </section>

    <section class="chapter" data-stop="mist" aria-labelledby="d3">
      <h2 id="d3"><small>Day three</small>Quiet water</h2>
      <ol class="moments">
        <li><time>8:30</time><p><strong>Guided kayaking</strong> through one of the calmest corners of the bay.</p></li>
        <li><time>Or</time><p>Stay in the jacuzzi, on the sundeck or in bed. Your cabin's yours until lunch.</p></li>
        <li><time>10:30</time><p>Last lunch on board, then back to Hanoi.</p></li>
        <li><time>4:30</time><p>Back at the hostel, with a camera roll full of photos and a few new numbers.</p></li>
      </ol>
      {img('g-kayaks', 'Two kayaks paddling across turquoise water beneath a limestone cliff')}
    </section>
  </div>
''' + included(['Two nights in your cabin on the Hideaway', 'Every meal on the itinerary'] + BASE_INCL[:1] + ['Cycling, trekking, kayaking, banana tubing, swimming and beach volleyball'] + BASE_INCL[1:], EXCL, 3) + before(3) + others(3)

tour6 = head(6, 'The bay,', 'then the mountains.', 'Two sides of northern Vietnam in six days: the full Hideaway cruise, then three days riding the Ha Giang Loop and staying with local families.') + f'''
  <div class="route" id="itinerary">
    <section class="chapter" data-stop="midday" aria-labelledby="d1">
      <h2 id="d1"><small>Days one to three</small>The full Hideaway cruise</h2>
      <ol class="moments">
        <li><time>Day 1</time><p>Into Lan Ha Bay. Beach stop, boat jumping, banana tubing, beach volleyball, jacuzzis, <strong>sunset party</strong> and BBQ.</p></li>
        <li><time>Day 2</time><p>Cycle through Viet Hai village, trek the Cat Ba jungle, fish massage lunch, then <strong>sunset party, round two</strong>.</p></li>
        <li><time>Day 3</time><p>Morning kayaking if you're up for it, lunch on board, back in Hanoi around 4:30pm.</p></li>
      </ol>
      <p class="route-link"><a class="more" href="tour-3-days.html">See the cruise hour by hour</a></p>
      {img('g-banana', 'Guests laughing on a banana boat in front of karst islands')}
    </section>

    <section class="chapter" data-stop="night" aria-label="Night bus north">
      <p class="says">Then a night bus north.</p>
      <ol class="moments">
        <li><time>7:30pm</time><p>Sleeper bus from Hanoi to Ha Giang.</p></li>
        <li><time>3:00am</time><p>Arrive in Ha Giang and sleep. That first bed is free.</p></li>
      </ol>
    </section>

    <section class="chapter" data-stop="mist" aria-labelledby="d4">
      <h2 id="d4"><small>Day four</small>Ha Giang to Du Gia</h2>
      <ol class="moments">
        <li><time>120km</time><p>Over <strong>Quan Ba pass</strong>, through the Dong Van Geopark and Tam Son.</p></li>
        <li><time>Night</time><p>Homestay with a local ethnic minority family in Du Gia.</p></li>
      </ol>
      {img('ha.giang.buffalo.motorbike.tour.jpg', 'Motorbikes on the Ha Giang Loop')}
    </section>

    <section class="chapter" data-stop="golden" aria-labelledby="d5">
      <h2 id="d5"><small>Day five</small>Du Gia to Dong Van</h2>
      <ol class="moments">
        <li><time>Ride</time><p>Through Meo Vac, then a <strong>boat trip on the Nho Que river</strong>.</p></li>
        <li><time>Pass</time><p>Over <strong>Ma Pi Leng pass</strong> to Dong Van.</p></li>
        <li><time>Night</time><p>Hotel or homestay in Dong Van, with a hot pot dinner if you want it.</p></li>
      </ol>
    </section>

    <section class="chapter" data-stop="dusk" aria-labelledby="d6">
      <h2 id="d6"><small>Day six</small>Back to Ha Giang City</h2>
      <ol class="moments">
        <li><time>150km</time><p>Sa Phin palace and Yen Minh, then back over Tam Son and Quan Ba pass.</p></li>
        <li><time>5:00pm</time><p>Bus back to Hanoi, with a free hostel bed when you get in and breakfast the next morning (until 9:30am).</p></li>
      </ol>
    </section>
  </div>
''' + included(['Two nights on the Hideaway, then homestays on the loop', 'Every meal on the tour', 'Sleeper buses to and from Ha Giang', 'Motorbike and fuel', 'Tour guide', 'Kayaking, banana tubing, swimming and beach volleyball', 'Entrance fees'],
               'Drinks, tips, travel insurance and personal spending.', 6) + before(6) + others(6)

# ================================================================== GALLERY
# One day on the boat, told left to right. To add photos, add a line to REEL:
# ('photo', file, alt text, caption, shape, size/offset)   shape = width/height ratio
# ('text', time label, line of text)
REEL = [
    ('text',  'Arrival', 'Hanoi to the bay. <b>Phones out.</b>'),
    ('photo', 'g-boat', 'The Hideaway Cruise anchored among the limestone islands of Lan Ha Bay', 'The Hideaway, anchored out in the bay.', '4/5', 'big'),
    ('text',  'Afternoon', 'First swim. <b>Nobody stays dry.</b>'),
    ('photo', 'g-backflip', 'A guest backflipping off the boat into the bay while another watches', 'Boat jumping. Style points optional.', '4/5', 'up'),
    ('photo', 'g-banana', 'Four guests in life jackets laughing on a banana boat in front of karst islands', 'Banana tubing, day one.', '4/5', 'down'),
    ('photo', 'g-beach-group', 'A big group of backpackers posing on the beach next to the day boat', 'Beach stop. Strangers this morning.', '16/9', ''),
    ('text',  'Sunset', 'Happy hour <b>on the top deck.</b>'),
    ('photo', 'g-deck', 'Guests with cocktails on the top deck at sunset, islands behind them', 'Cocktails on the top deck.', '4/5', 'up'),
    ('photo', 'g-lamp', 'A deck lamp glowing as the sun drops behind a karst island', 'Lights on as the sun drops behind the islands.', '4/5', 'small down'),
    ('text',  'After dark', 'Lights down. <b>Volume up.</b>'),
    ('photo', 'g-beerpong', 'Guests playing beer pong under a string of world flags', 'Beer pong under the flags.', '4/5', 'up'),
    ('photo', 'g-karaoke', 'A guest singing karaoke on the light-up dance floor', 'Karaoke, sung with total commitment.', '4/5', 'down'),
    ('photo', 'g-dance', 'Guests dancing and singing on the glowing dance floor', 'The dance floor lights up. Literally.', '4/5', 'big'),
    ('text',  'Day two', 'Cat Ba <b>on two wheels.</b>'),
    ('photo', 'g-cycle-road', 'A group cycling up a quiet road between jungle-covered cliffs on Cat Ba', 'Cycling through Cat Ba National Park.', '4/5', 'big'),
    ('photo', 'g-cyclists', 'Three cyclists stopping to look up at the jungle on Cat Ba', 'A stop on the ride.', '4/5', 'down'),
    ('text',  'Last morning', 'Quiet water. <b>Kayaks out.</b>'),
    ('photo', 'g-kayaks', 'Two kayaks paddling across turquoise water beneath a limestone cliff', 'Kayaking on the calm side of the bay.', '4/5', 'up'),
    ('text',  'Ha Giang Loop', '6-day tour: <b>then the mountains.</b>'),
    ('photo', IMG + 'ha.giang.buffalo.motorbike.tour.jpg', 'Motorbikes on the Ha Giang Loop', 'Three days on two wheels up north.', '3/2', 'down'),
]
REEL_STOPS = 'dawn,midday,midday,golden,sunset,night,night,midday,mist,dusk'


def frame(item):
    if item[0] == 'text':
        _, t, line = item
        return f'<div class="interlude" data-time="{t}"><span class="t">{t}</span><p>{line}</p></div>'
    _, file, alt, cap, ar, size = item
    oe = "this.closest('.zoom').classList.add('missing')"
    if file.startswith('http'):
        src = f'src="{file}" referrerpolicy="no-referrer"'
    else:
        base = f'assets/media/gallery/{file}'
        src = (f'src="{base}.jpg" srcset="{base}-sm.jpg {"1000w" if ar == "16/9" else "800w"}, {base}.jpg {"1920w" if ar == "16/9" else "1200w"}" '
               f'sizes="(max-width: 900px) 92vw, {"70vw" if ar == "16/9" else "40vw"}"')
    return (f'<figure class="frame {size}"><button class="zoom" type="button" style="--ar:{ar}" aria-label="View larger: {alt}">'
            f'<img {src} alt="{alt}" loading="lazy" decoding="async" onerror="{oe}"></button>'
            f'<figcaption>{cap}</figcaption></figure>')


reel = '\n        '.join(frame(x) for x in REEL)
gallery = f'''
  <section class="gal-head" data-stop="dawn">
    <h1 class="display"><span>The trip,</span><span class="heavy">in pictures.</span></h1>
    <p class="lede">From the first jump to the last paddle. Tap any photo to see it full screen. Been on the boat? Tag #halonghideaway and we might share yours.</p>
  </section>

  <section data-stop="dawn" style="padding-bottom:4vh">
    <figure class="film has-preview">
      <img src="assets/media/gallery/g-beach-group.jpg" alt="A big group of Hideaway guests on the beach next to the day boat">
      <div class="yt-preview" aria-hidden="true"></div>
      <a class="play" data-watch href="#" target="_blank" rel="noopener"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M4 2.5v13l11-6.5z" fill="currentColor"/></svg>Watch with sound</a>
      <figcaption>The Hideaway in under a minute</figcaption>
    </figure>
  </section>

  <section class="reel-sec" data-stops="{REEL_STOPS}" aria-label="A day on the boat, in photos">
    <div class="reel-pin">
      <div class="reel-hud" aria-hidden="true"><span class="reel-now">Morning</span><span class="reel-bar"><i></i></span><span class="reel-hint">Keep scrolling</span></div>
      <div class="reel-track">
        {reel}
        <div class="interlude" data-time="Your turn"><span class="t">Your turn</span><p>Want to be <b>in the next photos?</b></p><a class="btn" href="tours.html">Find my trip</a></div>
      </div>
    </div>
  </section>
'''

VIEWER = '''<dialog id="viewer" aria-label="Photo viewer">
  <button class="close" type="button">Close</button>
  <div class="v-stage"><img src="" alt=""></div>
  <button class="v-prev" type="button" aria-label="Previous photo"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M11.5 3 5.5 9l6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>
  <button class="v-next" type="button" aria-label="Next photo"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M6.5 3l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>
  <div class="v-bar"><span class="v-cap"></span><span class="v-count"></span></div>
</dialog>'''

pages = {
    'index.html': ('Halong Hideaway | Come as strangers, leave as friends',
                   'A party cruise on Lan Ha Bay for backpackers. Jacuzzis on deck, a sunset party every night, kayaks in the morning. Leaves Hanoi daily.', home, ''),
    'about.html': ('About us | Halong Hideaway', 'Halong Hideaway is run by the team behind Central Backpackers and Buffalo Hostels.', about, ''),
    'tours.html': ('Tours | Halong Hideaway', 'Compare the 2-day, 3-day and 6-day Halong Hideaway tours.', tours, ''),
    'tour-2-days.html': ('2 days, 1 night | Halong Hideaway', 'One night on Lan Ha Bay: beach stop, sunset party, BBQ and morning kayaking. 3,150,000₫.', tour2, bookbar(2)),
    'tour-3-days.html': ('3 days, 2 nights | Halong Hideaway', 'The full Hideaway: two sunset parties, Cat Ba cycling and trekking, kayaking. 4,900,000₫.', tour3, bookbar(3)),
    'tour-6-days.html': ('6 days with the Ha Giang Loop | Halong Hideaway', 'The full Hideaway cruise plus three days riding the Ha Giang Loop. From 8,800,000₫.', tour6, bookbar(6)),
    'gallery.html': ('Gallery | Halong Hideaway', 'Photos and video from the Halong Hideaway cruise and the Ha Giang Loop.', gallery, VIEWER),
}
for f, (t, d, b, x) in pages.items():
    (OUT / f).write_text(shell(f, t, d, b, x))
print('built', len(pages))
