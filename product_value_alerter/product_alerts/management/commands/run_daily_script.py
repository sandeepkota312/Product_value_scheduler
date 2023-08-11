from django.core.management.base import BaseCommand
import schedule
import time
from ...models import URLs_Feed
import requests as req
from bs4 import BeautifulSoup

def fetch_product_latest_price():
    # Your script logic 
    print("Running the daily script!")
    Url_objects=URLs_Feed.objects.all()
    for Url_object in Url_objects:
        url=Url_object.Url
        r=req.get(url)
        time.sleep(2)
        while r.status_code==503:
            r=req.get(url)
            time.sleep(3)
        if r.status_code==200:
            soup=BeautifulSoup(r.content,'lxml')
            Current_price=soup.find('span',class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay").find('span',class_="a-price-whole").get_text().split(',')
            Str=''
            for x in Current_price:
                Str+=x
            Current_price=int(Str)
            if Url_object.Current_price>Current_price:
                if Url_object.lowest_price>Current_price:
                    Url_object.lowest_price=Current_price
                    Url_object.Current_price=Current_price
                    Url_object.save()
                    print(Url_object.product_name+'Lowest price ever..!!')
                else:
                    Url_object.Current_price=Current_price
                    Url_object.save()
                    print('Price drop..!!')
            elif Url_object.Current_price<Current_price:
                Url_object.Current_price=Current_price
                Url_object.save()
                print('Price increased :(')
            else:
                print('No price Change..!')
                pass
            
        else:
            print('site '+ f'{url}' + ' was not hit. Code:',r.status_code)

class Command(BaseCommand):
    help = 'Runs a daily script'

    def handle(self, *args, **options):
        schedule.every().day.at("21:05").do(fetch_product_latest_price)  # Adjust the time as needed
        print('Scheduler started :)')
        while True:
            schedule.run_pending()
            time.sleep(1)
