
import socket
import uuid
import geocoder
import requests

def cach_user_device_info():
    hostname, ip_address, mac_address, location = None
    """
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        #mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
        #location = geocoder.ip(ip_address).address

        return hostname, ip_address, mac_address, location
    except socket.error as e:
        #print("Socket error:", e)
        return hostname, ip_address, mac_address, location
    except uuid.error as e:
        #print("UUID error:", e)
        return hostname, ip_address, mac_address, location
    except geocoder.GeocoderError as e:
        #print("Geocoder error:", e)
        return hostname, ip_address, mac_address, location
    except Exception as e:
        #print("An error occurred:", e)
        return hostname, ip_address, mac_address, location
    """
    

def cach_user_device_info_with_api():
    hostname, ip_address, mac_address, location = None
    try:
        ip_address = requests.get('https://api.ipify.org')
        return ip_address, None, None, None
    except Exception as e:
        #print("An error occurred:", e)
        return hostname, ip_address, mac_address, location
    