import click
import logic

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        try:
            user_requirement = click.prompt("Please enter the functional requirement")
            ctx.invoke(test_and_code, user_requirement=(user_requirement,))
        except Exception as e:
            click.echo(f"An error occurred: {str(e)}")

@cli.command()
@click.argument('outputfolder')
def outputfolder(outputfolder):
    try:
        logic.set_output_folder(outputfolder)
        click.echo(f'Output folder set to {outputfolder}')
    except Exception as e:
        click.echo(f"Failed to set output folder. Error: {str(e)}")

@cli.command()
@click.argument('model_name', type=click.Choice(['text-davinci-003', 'gpt-3.5-turbo', 'gpt-4'], case_sensitive=False))
def model(model_name):
    try:
        logic.set_model(model_name)
        click.echo(f'Model set to {model_name}')
    except Exception as e:
        click.echo(f"Failed to set model. Error: {str(e)}")

@cli.command()
@click.argument('user_requirement', nargs=-1)
def test_and_code(user_requirement):
    user_requirement_str = ' '.join(user_requirement)
    comment, output = logic.generate_and_save_logic(user_requirement_str)
    if output:
        click.echo(f"\nGenerated test for function: {output['function_name']}")
        click.echo(f"..also generated function: {output['function_name']}")
    else:
        click.echo(comment)

@cli.command()
@click.argument('user_requirement', nargs=-1)
def test(user_requirement):
    user_requirement_str = ' '.join(user_requirement)
    comment, _ = logic.generate_and_save_logic(user_requirement_str, save_function_code=False)
    click.echo(comment)

if __name__ == "__main__":
    cli()
