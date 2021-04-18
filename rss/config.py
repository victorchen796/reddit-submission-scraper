from resources import get_config, update_config


"""
config:
{
  'client_id': '<client_id>',
  'client_secret': '<client_secret>',
  'user_agent': '<user_agent>'
}
"""
config = get_config()


def view():
    return config


def edit(client_id, client_secret, user_agent):
    config['client_id'] = client_id
    config['client_secret'] = client_secret
    config['user_agent'] = user_agent
    update_config(config)


def clear():
    edit(None, None, None)
