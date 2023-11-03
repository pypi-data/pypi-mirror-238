# test_cli.py
import os
from click.testing import CliRunner
from dog_cli.main import cli

def test_list_all():
    runner = CliRunner()
    result = runner.invoke(cli, [' list_all'])  # Utilisez le nom de la commande telle que définie dans le décorateur @cli
    assert result.exit_code == 0, "La commande a échoué avec un code de sortie non nul"
    assert "Error fetching breeds." not in result.output, "La commande a retourné une erreur en récupérant les races"
   

def test_get_image():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['get-image', '--breed', 'bulldog', '--file', 'test_image.jpg'])
        assert result.exit_code == 0, f"La commande a échoué avec un code de sortie non nul: {result.output}"
        assert 'Image saved to test_image.jpg' in result.output, "Le message attendu de confirmation de sauvegarde d'image n'est pas présent dans la sortie."
        assert os.path.exists('test_image.jpg'), "Le fichier d'image n'a pas été créé."

