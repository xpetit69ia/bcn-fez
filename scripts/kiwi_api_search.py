#!/usr/bin/env python3
"""Search Kiwi.com public offers through API.SH and normalize results."""
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://api.api.sh/kiwi/v1/flights"

def main():
    key = os.environ.get("APISH_API_KEY")
    if not key:
        raise SystemExit("Missing APISH_API_KEY GitHub Actions secret")

    origin = os.environ.get("ORIGIN", "BCN").strip().upper()
    destination = os.environ.get("DESTINATION", "FEZ").strip().upper()
    selected = dt.date.fromisoformat(os.environ["DEPARTURE_DATE"])
    start, end = selected - dt.timedelta(days=7), selected + dt.timedelta(days=7)
    params = {
        "from": origin, "to": destination,
        "date": start.isoformat(), "date_end": end.isoformat(),
        "adults": 1, "cabin": "economy", "currency": "EUR",
        "market": "es", "sort": "price", "size": 50, "page": 1,
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"x-api-key": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"API.SH HTTP {exc.code}: {detail}")
    if payload.get("success") is False:
        raise SystemExit("API.SH returned an error: " + str(payload.get("error", payload)))

    offers = []
    for item in payload.get("itineraries", []):
        outbound = item.get("outbound") or {}
        departure = item.get("departure") or outbound.get("departure")
        if not departure:
            continue
        departure_date = str(departure)[:10]
        if not (start.isoformat() <= departure_date <= end.isoformat()):
            continue
        carrier = None
        legs = outbound.get("legs") or []
        if legs and isinstance(legs[0], dict):
            first_leg = legs[0]
            carrier_value = first_leg.get("carrier")
            if isinstance(carrier_value, dict):
                carrier = carrier_value.get("name") or carrier_value.get("code")
            elif isinstance(carrier_value, str):
                carrier = carrier_value
            carrier = carrier or first_leg.get("airline")
        if not carrier:
            carrier = item.get("provider") or "Kiwi.com"
        offers.append({
            "source": "Kiwi.com via API.SH",
            "provider": item.get("provider", "Kiwi.com"),
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "departure": departure,
            "arrival": outbound.get("arrival") or item.get("arrival"),
            "carrier": carrier,
            "price": item.get("price_eur") if item.get("price_eur") is not None else item.get("price"),
            "currency": "EUR" if item.get("price_eur") is not None else item.get("currency", "EUR"),
            "duration_seconds": item.get("duration_seconds"),
            "stops": outbound.get("stops", item.get("stops")),
            "included_hand_bags": item.get("included_hand_bags"),
            "included_checked_bags": item.get("included_checked_bags"),
            "self_transfer": item.get("self_transfer"),
            "booking_url": (item.get("booking_options") or [{}])[0].get("url"),
            "status": "unverified",
        })

    result = {
        "source": "Kiwi.com via API.SH",
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "origin": origin, "destination": destination,
        "selected_date": selected.isoformat(),
        "date_from": start.isoformat(), "date_to": end.isoformat(),
        "credits_used": payload.get("credits_used"),
        "cached": payload.get("cached"),
        "offers": sorted(offers, key=lambda x: (x["departure_date"], x["price"] or 10**9)),
        "note": "Tarifas observadas en Kiwi.com; no son precios confirmados por la aerolínea.",
    }
    out = pathlib.Path("data/kiwi-results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Kiwi/API.SH: {len(offers)} ofertas para {origin} → {destination}, {start} a {end}.")
    print(f"Créditos declarados por el proveedor: {payload.get('credits_used', 'no informado')}")

if __name__ == "__main__":
    main()
