from importlib.metadata import files
import json
import requests
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        meta_data_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(meta_data_file_name).exists():
            print(f"{meta_data_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating metadata file {meta_data_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_file_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_file_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            collectible_metadata["image"] = image_uri
            print(collectible_metadata)
            with open(meta_data_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(meta_data_file_name)


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        response = requests.post(ipfs_url + end_point, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        file_name = file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={file_name}"
        # https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json
        print(image_uri)
        return image_uri
