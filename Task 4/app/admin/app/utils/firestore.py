#Cloud Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from datetime import datetime, timedelta

#Firestore init
certificate={
  "type": "service_account",
  "project_id": "centralised-smart-parking",
  "private_key_id": "70d0636166264d272407c29d00566455467dc589",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCyCmZr2s0XuiPY\nhnpxw+xIh1ippj53yFy9/s+TJElrCEiPguwjGe2yP49R3wIH/lYwSUfHhvRgWd4n\neiRg2ssXNFXQC5467TMvdkdOOwyWLex9JvN9tonef+VAKg5BIAg8qpJq1Y3202/A\nTOOVLDvqKE5vq7PVLtLWgp06AobzcAjo6cFJX8pjRJsc0Bsg5SnF2snhyVvFEstT\nWTXOAL4FNP0BkuTJNVqvVsRTA+rp/jxBXTwBiShU2YqemQ09yj7LAHUPjtBcnuVS\nu1Sulzziy3ihWXvoM8ZSqM0C9ZiEs+l0jzsusTt7/0XIO+Bbem7rhRqsliZiUCzZ\nNbYWwgDzAgMBAAECggEANmXnFV0s/OrquOWd09TBBQgVlwAsZfzaGVMZqSOVKxbE\n1NRzweXSMnwpFiLFRBv5yZcaT2R0llve/MDdDJrNIrHi5kYmemqvEPlaoBR6rAgs\nEbEtBGQZi9oX+Zrf8BYRbjfPtMS7M4c2xdK4VoPFaq4WCRi1QZWk5dXSpD7RbN9y\nbxjPTp3X0xTCzxO8AsuvLW6jXsbtj9KESepxdOeojlpcXxlENqNDzY9pHk+BVzf7\nnVWoi+hrvFE6a8dCj6QJbMWjgDYdmjxksmy6WXbYGNntjjHS7Cj3LEVKxrszUp4e\nqxaEWblZ3un7wEC5gTtnlpkH65bnXUAIsrM39FTgQQKBgQD31y0TupicNJcSEzuq\nf7IFsh2Wx78KU17HKFRCjdSdFjx9Xx7YW08/wZETVyMWV1PzEPoDPgCir9X1VEQO\nYodnbHsu0nNuib/7HGYnLMXhDWHQwWhK8+DGnXCCmCozrfdtb+kJCV8q0E4BJZbm\nKLg2htK4wt5oaI/XFb2Pz+IFdQKBgQC35vGTYc//BUyaek7aGKncD0RMMVSEFl5b\njvXfUJ/wYJA+QsCCdV8rluXSw7hVQQfvhrF9rbxhlRj5qaIIE1O0Er7ALkGPOvao\nJ/7loRlxuZFB5xwH94whFerG1lBT/a96kiJ4Tg5p9JEedRLnJlIC+qCa7LLltVXj\n/wwCLcFXxwKBgQDnPiGU8tlJhdgeyUs2fgbAQbxR3vVk0PzxnbNglaz3FLRD1eiV\nvjxnJFgUT40xXzG47PIY7FTzdlSPnpwRP+VOnm0g9sM1M9molorJqoDGxxGpEYwZ\nwwrKxkMf1pIpvfvKZExuXgwpikn9z/DHtt6KIamjMk8J4+WxrVs9P52HsQKBgQCy\nFzoWygBNLOqUJqG532yPKVGwn40DJU5XSEie7EsW08ycHrSjIdr6MXV6+ALIvONc\neInl9ZuavHKlRDsfqufCWOzU23atqCI5khHsemhTk6sxsQeaR4YyfDESQXUlAWUw\nQ9iRvLWEskzeu+2EX73IGMHzhglxHnyBAPq2GW1E/QKBgDgGs7jVh9Q38GLOZwy4\nElJ1XMejtoj5hVU32pU2r9+AAO5jxrhE6wRLhUHCZZ3K0YWN8clj6S7s/yqg/2DE\nf6UzlmtdfuJzjJGna+mnuby3bbeVz7KpdG1iKcm1ia7yJlxX7qicHYD5Hkwvy2mu\n581rUaxWgjGGBuYytv+Plc1l\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-1v7o2@centralised-smart-parking.iam.gserviceaccount.com",
  "client_id": "110022476516174221125",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-1v7o2%40centralised-smart-parking.iam.gserviceaccount.com"
}
cred = credentials.Certificate(certificate)
firebase_admin.initialize_app(cred)

#get db reference
db = firestore.client()

#get provider name form region&province
def getProviderName(region: str, province: str):
    return db.collection(u'Parkings').document(region).collection(province).document(u'_PROVIDER_DATA').get().to_dict()["providerName"]

#get parkings dict from region&province
def getParkingsList(region, province):
    firestore_parkings_collection = db.collection(u'Parkings').document(region).collection(province).stream()#get parkings collection from Firestore

    #build dictionary
    parkings_dict={}
    for parking in firestore_parkings_collection:
        if(parking.id != "_PROVIDER_DATA"):#process parkings only
            parking_id=parking.id#save parking's id
            parking=parking.to_dict()#convert parking's Firestore CollectionRef to python-dictionary
            parkings_dict[parking_id]=parking#add parking to parkings dictionary
    return parkings_dict

#get tickets dict from province
def getTicketsList(province):
    firestore_parkings_collection=db.collection(u'Tickets').where(u'province', u'==', province).stream()#get compliant tickets from Firestore

    #build dictionary
    parkings_dict={}
    for parking in firestore_parkings_collection:
        if(parking.id != "_PROVIDER_DATA"):#process parkings only
            parking_id=parking.id#save parking's id
            parking=parking.to_dict()#convert parking's Firestore CollectionRef to python-dictionary
            parkings_dict[parking_id]=parking#add parking to parkings dictionary
    return parkings_dict

def insertParking(region, province, parking_name, latitude, longitude, capacity, price_per_hour, type, ElectricVehicleChargingStation, GuardedByHuman, GuardedByCameras):
    document_ref = db.collection(u'Parkings').document(region).collection(province).document()#get db location where insert data
    document_ref.set({ u'parking_name': parking_name, u'location': firebase_admin.firestore.GeoPoint(float(latitude), float(longitude)), u'capacity': int(capacity), u'price_per_hour': float(price_per_hour), u'features': { u'ElectricVehicleChargingStation': ElectricVehicleChargingStation, u'GuardedByCameras': GuardedByCameras, u'GuardedByHuman': GuardedByHuman, u'type': int(type) } })#set parking specs
    parking_id = document_ref.id
    document_ref.collection(u'realtime_data').document(u'disponibility').set({ u'free': int(capacity) })#set realtime data
    return parking_id

def deleteParking(region, province, parking_id):
    db.collection(u'Parkings').document(region).collection(province).document(parking_id).collection(u'realtime_data').document(u'disponibility').delete()
    db.collection(u'Parkings').document(region).collection(province).document(parking_id).delete()

def updateParking(region, province, parking_id, parking_name, latitude, longitude, capacity, price_per_hour, type, ElectricVehicleChargingStation, GuardedByHuman, GuardedByCameras):
    document_ref = db.collection(u'Parkings').document(region).collection(province).document(parking_id)
    document_ref.update({ u'parking_name': parking_name, u'location': firebase_admin.firestore.GeoPoint(float(latitude), float(longitude)), u'capacity': int(capacity), u'price_per_hour': float(price_per_hour), u'features': { u'ElectricVehicleChargingStation': ElectricVehicleChargingStation, u'GuardedByCameras': GuardedByCameras, u'GuardedByHuman': GuardedByHuman, u'type': int(type) } })#set parking specs
