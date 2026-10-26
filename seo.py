"""Structured data generated from the same content as the visible site."""
import json
import re
import unicodedata


def json_ld(value):
    payload = json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return '<script type="application/ld+json">' + payload + '</script>'


def item_id(category, name):
    text = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return category + '-' + re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def restaurant(site_url, media, socials):
    return {
        '@type': 'Restaurant', '@id': site_url + '/#ristorante',
        'name': 'Sorriso Bistrot', 'url': site_url + '/',
        'description': 'Pizzeria a Roma San Basilio, in Via Sarnano 4. Pizza classica napoletana e impasti senza glutine di nostra produzione, preparati in un laboratorio separato. Tavoli, asporto e consegna a domicilio.',
        'telephone': '+393455834226',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Via Sarnano 4', 'postalCode': '00156', 'addressLocality': 'Roma', 'addressRegion': 'Lazio', 'addressCountry': 'IT'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 41.9391098, 'longitude': 12.5781278},
        'hasMap': 'https://www.google.com/maps/search/?api=1&query=Sorriso+Bistrot+Via+Sarnano+4+Roma',
        'logo': site_url + '/img/logo-sorriso-web.webp',
        'image': [site_url + '/' + media[key]['variants'][-1]['src'] for key in ('home/sala', 'home/cottura', 'home/fritti')],
        'servesCuisine': ['Pizza', 'Italiana', 'Senza glutine'],
        'menu': site_url + '/menu.html',
        'hasMenu': {'@id': site_url + '/menu.html#menu'},
        'acceptsReservations': True,
        'sameAs': [social['profile'] for social in socials if social.get('profile')],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '18:00', 'closes': '23:00'}],
    }


def offers(item):
    def simple_price(value):
        match = re.fullmatch(r'€\s*(\d+(?:[,.]\d{1,2})?)', value or '')
        return match.group(1).replace(',', '.') if match else None

    result = []
    if item.get('pg'):
        for label, raw in (('Classica', item.get('pc')), ('Senza glutine', item['pg'])):
            price = simple_price(raw)
            if price:
                result.append({'@type': 'Offer', 'name': label, 'price': price, 'priceCurrency': 'EUR'})
    else:
        raw = item.get('pc') or ''
        price = simple_price(raw)
        if price:
            result.append({'@type': 'Offer', 'price': price, 'priceCurrency': 'EUR'})
        else:
            for part in raw.split('·'):
                match = re.fullmatch(r'\s*(\d+)cl\s+€(\d+(?:[,.]\d{1,2})?)\s*', part)
                if match:
                    result.append({'@type': 'Offer', 'name': match.group(1) + ' cl', 'price': match.group(2).replace(',', '.'), 'priceCurrency': 'EUR'})
    return result


def structured_data(page, title, description, site_url, media, socials, categories):
    page_url = site_url + ('/' if page == 'index.html' else '/' + page)
    business = restaurant(site_url, media, socials)
    website = {'@type': 'WebSite', '@id': site_url + '/#sito', 'name': 'Sorriso Bistrot', 'url': site_url + '/', 'inLanguage': 'it-IT', 'publisher': {'@id': business['@id']}}
    webpage = {'@type': 'WebPage', '@id': page_url + '#pagina', 'url': page_url, 'name': title, 'description': description, 'inLanguage': 'it-IT', 'isPartOf': {'@id': website['@id']}, 'about': {'@id': business['@id']}}
    graph = [business, website, webpage]
    if page == 'menu.html':
        sections = []
        for category in categories:
            items = []
            for item in category['items']:
                identifier = page_url + '#' + item_id(category['id'], item['n'])
                entry = {'@type': 'MenuItem', '@id': identifier, 'url': identifier, 'name': item['n'], 'description': item['d']}
                prices = offers(item)
                if prices:
                    entry['offers'] = prices
                if category['id'] in ('antipasti', 'dolci'):
                    entry['suitableForDiet'] = 'https://schema.org/GlutenFreeDiet'
                items.append(entry)
            sections.append({'@type': 'MenuSection', '@id': page_url + '#categoria-' + category['id'], 'name': category['t'], 'hasMenuItem': items})
        menu = {'@type': 'Menu', '@id': page_url + '#menu', 'name': 'Menù di Sorriso Bistrot', 'url': page_url, 'inLanguage': 'it-IT', 'hasMenuSection': sections}
        breadcrumbs = {'@type': 'BreadcrumbList', '@id': page_url + '#percorso', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Sorriso Bistrot', 'item': site_url + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Menù', 'item': page_url},
        ]}
        webpage['mainEntity'] = {'@id': menu['@id']}
        webpage['breadcrumb'] = {'@id': breadcrumbs['@id']}
        graph.extend([menu, breadcrumbs])
    else:
        webpage['mainEntity'] = {'@id': business['@id']}
    return json_ld({'@context': 'https://schema.org', '@graph': graph})
