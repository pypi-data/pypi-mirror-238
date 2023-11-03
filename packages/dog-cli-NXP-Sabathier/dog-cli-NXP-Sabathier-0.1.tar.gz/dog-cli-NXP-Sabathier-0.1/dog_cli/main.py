import click
import requests

BASE_URL = "https://dog.ceo/api"

@click.group()
def cli():
    """CLI for dog.ceo API"""
    pass

@cli.command()
def list_all():
    """List all dog breeds"""
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    if response.status_code == 200:
        breeds = response.json()['message']
        for breed, sub_breeds in breeds.items():
            if sub_breeds:
                for sub in sub_breeds:
                    click.echo(f"{sub} {breed}")
            else:
                click.echo(breed)
    else:
        click.echo("Error fetching breeds.")

@cli.command()
@click.option("--breed", required=True, help="Breed of the dog")
@click.option("--file", "output_file", required=True, type=click.Path(), help="Output file to save the image")
def get_image(breed, output_file):
    """Download image of a specific breed"""
    breed = breed.lower()
    response = requests.get(f"{BASE_URL}/breed/{breed}/images/random")
    if response.status_code == 200:
        image_url = response.json()['message']
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            with open(output_file, 'wb') as f:
                for chunk in image_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            click.echo(f"Image saved to {output_file}")
        else:
            click.echo("Error fetching the image.")
    else:
        click.echo(f"Error fetching the breed {breed}.")


if __name__ == "__main__":
    cli()
