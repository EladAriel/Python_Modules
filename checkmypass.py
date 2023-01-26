"""
This script has been written based on the "Complete Python Developer in 2022: Zero to Mastery" course.
"""

# Import libraries
import requests
import hashlib
import sys

def request_api_data(query_char):
    """

    :param query_char: Query characters
    :return: Response
    """
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    # Get response
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    """

    :param hashes: All passwords that match the first five characters of the user's password.
    :param hash_to_check: All passwords characters except for the first five.
    :return: Number of times a password has been compromised.
    """
    # Get all passwords that match to first5_char
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    """

    :param password: Password from user's input
    :return: Password leaks count
    """
    # Create SHA1 password
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    # Check password if it exists in API response
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    """

    :param args: All passwords from user's input
    :return: Advice on whether to change the password or not
    """
    # Loop over all passwords given by user
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times. You should change your password')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
