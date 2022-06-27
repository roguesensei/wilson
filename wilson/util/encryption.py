import os
import pickle
import rsa


def generate_keys(server_id: int) -> tuple[rsa.PublicKey, rsa.PrivateKey]:
    public_key, private_key = rsa.newkeys(512)
    os.mkdir(f'.wilson/{server_id}')

    with open(f'.wilson/{server_id}/key.pub', 'wb') as f:
        pickle.dump(public_key, f, pickle.HIGHEST_PROTOCOL)
    with open(f'.wilson/{server_id}/key.rsa', 'wb') as f:
        pickle.dump(private_key, f, pickle.HIGHEST_PROTOCOL)

    return public_key, private_key


def write_settings(server_id: int):
    with open(f'.wilson/{server_id}/key.pub', 'rb') as f:
        key = pickle.load(f)
        data = rsa.encrypt('Test'.encode(), key)
        with open(f'.wilson/{server_id}/dat', 'wb') as dat:
            dat.write(data)


def read_settings(server_id: int):
    with open(f'.wilson/{server_id}/key.rsa', 'rb') as f:
        key = pickle.load(f)
        with open(f'.wilson/{server_id}/dat', 'rb') as dat:
            data = rsa.decrypt(dat.read(), key)
            return data.decode()
