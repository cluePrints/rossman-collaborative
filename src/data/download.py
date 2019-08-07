import requests
import click
import tarfile

@click.command()
@click.argument('url')
@click.argument('folder', type=click.Path())
def download_file(url, folder):
   filename = url.split('/')[-1]

   print(f'Downloading from {url} to {folder}')
   response = requests.get(url)

   dest_file = f'{folder}/{filename}'
   with open(dest_file,  'wb') as ofile:
       ofile.write(response.content)

   print(f'Extracting {dest_file} to {folder}')
   tar = tarfile.open(dest_file)
   tar.extractall(path=folder)

if __name__ == '__main__':
   download_file()
