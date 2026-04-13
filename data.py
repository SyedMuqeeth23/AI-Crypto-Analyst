import requests
import time

# 🔹 Simple Request Cache (in-memory)
_cache = {}
_cache_ttl = 300  # 5 minutes

def _get_cached(key):
    """Get value from cache if not expired"""
    if key in _cache:
        value, timestamp = _cache[key]
        if time.time() - timestamp < _cache_ttl:
            return value
    return None

def _set_cached(key, value):
    """Set cache with timestamp"""
    _cache[key] = (value, time.time())

# 🔹 Base URL
BASE_URL = "https://api.coingecko.com/api/v3"

# 🔹 Fallback Demo Data (for rate limiting or testing)
FALLBACK_PRICES = {
    "bitcoin": {"name": "BITCOIN", "price": 65420.50, "change": 2.34},
    "ethereum": {"name": "ETHEREUM", "price": 3240.75, "change": 1.89},
    "cardano": {"name": "CARDANO", "price": 1.12, "change": -0.45},
    "solana": {"name": "SOLANA", "price": 189.50, "change": 3.21},
    "polkadot": {"name": "POLKADOT", "price": 8.95, "change": 0.67},
    "ripple": {"name": "RIPPLE", "price": 2.45, "change": 1.23},
    "dogecoin": {"name": "DOGECOIN", "price": 0.38, "change": 5.67},
    "binancecoin": {"name": "BINANCE COIN", "price": 612.30, "change": 2.11},
}

FALLBACK_MOVERS = {
    "gainers": [
        {"name": "Dogecoin", "change": 5.67},
        {"name": "Solana", "change": 3.21},
        {"name": "Bitcoin", "change": 2.34},
    ],
    "losers": [
        {"name": "Cardano", "change": -0.45},
        {"name": "Ripple", "change": -1.23},
        {"name": "Polkadot", "change": -2.34},
    ]
}


# =========================================
# 🪙 1. Get price of ANY coin
# =========================================
def get_coin_price(coin_name):
    """
    Fetch price and 24h change for a given coin with caching and fallback
    Example: bitcoin, ethereum, dogecoin, binancecoin
    """
    cache_key = f"price_{coin_name.lower()}"
    cached_result = _get_cached(cache_key)
    if cached_result:
        return cached_result

    url = f"{BASE_URL}/simple/price"

    params = {
        "ids": coin_name.lower(),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        # Check for API errors
        if isinstance(data, dict) and "status" in data:
            # Rate limited - use fallback
            if coin_name.lower() in FALLBACK_PRICES:
                fallback = FALLBACK_PRICES[coin_name.lower()].copy()
                fallback["_fallback"] = True
                _set_cached(cache_key, fallback)
                return fallback
            return {"error": f"API Error: {data['status'].get('error_message', 'Unknown')}"}

        if coin_name.lower() not in data:
            return {"error": f"Coin '{coin_name}' not found"}

        coin = data[coin_name.lower()]

        result = {
            "name": coin_name.upper(),
            "price": coin.get("usd", 0),
            "change": round(coin.get("usd_24h_change", 0), 2)
        }
        
        _set_cached(cache_key, result)
        return result

    except requests.exceptions.Timeout:
        # Use fallback on timeout
        if coin_name.lower() in FALLBACK_PRICES:
            fallback = FALLBACK_PRICES[coin_name.lower()].copy()
            fallback["_fallback"] = True
            return fallback
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        if coin_name.lower() in FALLBACK_PRICES:
            fallback = FALLBACK_PRICES[coin_name.lower()].copy()
            fallback["_fallback"] = True
            return fallback
        return {"error": "Connection error. Check your internet."}
    except Exception as e:
        return {"error": str(e)}


# =========================================
# 📊 2. Get BTC + ETH (default quick view)
# =========================================
def get_major_coins():
    coins = ["bitcoin", "ethereum"]

    results = {}

    for coin in coins:
        data = get_coin_price(coin)
        if data:
            results[coin.upper()] = data

    return results


# =========================================
# 🚀 3. Top Gainers & Losers
# =========================================
def get_top_movers(limit=5):
    """
    Returns top gainers and losers in last 24h with caching and fallback
    """
    cache_key = f"movers_{limit}"
    cached_result = _get_cached(cache_key)
    if cached_result:
        return cached_result

    url = f"{BASE_URL}/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        # Check if API returned an error (e.g., rate limit)
        if isinstance(data, dict) and "status" in data:
            # Rate limited - use fallback
            fallback = FALLBACK_MOVERS.copy()
            fallback["_fallback"] = True
            _set_cached(cache_key, fallback)
            return fallback
        
        # Ensure data is a list
        if not isinstance(data, list):
            # Use fallback on invalid response
            fallback = FALLBACK_MOVERS.copy()
            fallback["_fallback"] = True
            return fallback

        # Sort by 24h change
        sorted_data = sorted(
            data,
            key=lambda x: x.get("price_change_percentage_24h") or 0,
            reverse=True
        )

        top_gainers = sorted_data[:limit]
        top_losers = sorted_data[-limit:]

        gainers = [
            {
                "name": coin["name"],
                "change": round(coin.get("price_change_percentage_24h", 0), 2)
            }
            for coin in top_gainers
            if isinstance(coin, dict) and "name" in coin
        ]

        losers = [
            {
                "name": coin["name"],
                "change": round(coin.get("price_change_percentage_24h", 0), 2)
            }
            for coin in top_losers
            if isinstance(coin, dict) and "name" in coin
        ]

        result = {
            "gainers": gainers,
            "losers": losers
        }
        
        _set_cached(cache_key, result)
        return result

    except requests.exceptions.Timeout:
        fallback = FALLBACK_MOVERS.copy()
        fallback["_fallback"] = True
        return fallback
    except requests.exceptions.ConnectionError:
        fallback = FALLBACK_MOVERS.copy()
        fallback["_fallback"] = True
        return fallback
    except Exception as e:
        fallback = FALLBACK_MOVERS.copy()
        fallback["_fallback"] = True
        return fallback


# =========================================
# 📰 4. Trending Coins (News-like signal)
# =========================================
def get_trending_coins():
    """
    Returns trending coins with caching
    """
    cache_key = "trending"
    cached_result = _get_cached(cache_key)
    if cached_result:
        return cached_result

    url = f"{BASE_URL}/search/trending"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        # Check for API errors
        if isinstance(data, dict) and "status" in data:
            return {"error": f"API Error: {data['status'].get('error_message', 'Unknown')}"}

        trending = []

        for coin in data.get("coins", [])[:5]:
            item = coin.get("item", {})
            if isinstance(item, dict):
                trending.append({
                    "name": item.get("name", "Unknown"),
                    "symbol": item.get("symbol", "?"),
                    "rank": item.get("market_cap_rank", "N/A")
                })

        _set_cached(cache_key, trending)
        return trending

    except requests.exceptions.Timeout:
        return {"error": "API request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error. Please check your internet."}
    except Exception as e:
        return {"error": str(e)}


# =========================================
# 🧠 5. Combined Market Snapshot (VERY USEFUL)
# =========================================
def get_market_summary():
    """
    Combines major coins + movers + trending
    """

    major = get_major_coins()
    movers = get_top_movers()
    trending = get_trending_coins()

    return {
        "major_coins": major,
        "top_movers": movers,
        "trending": trending
    }
    