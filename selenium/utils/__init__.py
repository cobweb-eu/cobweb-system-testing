import pprint

def convert_from_friendly_name(friendly_fieldname):
    """ Function to convert from a 'Friendly' feature property
        to one that can be used in web services. I.e., no spaces
        or special characters. This is reverse-engineered from
        the conversion that happens between authoring tool and
        uploaded survey data. Used for checking observations

        :type friendly_fieldname: String
        :param friendly_fieldname: Human readable field name for survey question
        :return: A new string representing the field as used witin surveys and
                 observations in the backend and WFS
    """

    # implementation below may have changed

    #return '_'.join([val.lower() if i > 0 else val
    #                 for i, val
    #                 in enumerate(friendly_fieldname.split(' '))])
    return friendly_fieldname.replace(' ', '_')


class Survey:
    """ Simple class to represent a survey as an id and name """
    def __init__(self, survey_id, survey_name):
        self.id = survey_id
        self.name = survey_name

    def __str__(self):
        return "('%s', '%s')"%(self.id, self.name)


class AuthUser(object):
    """ A utility object to represent a username and password
    """
    def __init__(self, username, password ):
        self.id = username
        self.pw = password


class CobwebUser(AuthUser):
    """ Simple class to extend AuthUser to include uuid """
    def __init__(self, username, password, uuid):
        self.uuid = uuid
        super(CobwebUser, self).__init__(username, password)


pp = pprint.PrettyPrinter(indent=4)


def parse_observation(observation):
    """ This function expects to take a list in the
        form ['key1: value', 'key2: value'] and return a
        dict of the keys and values
    """
    return {key.strip(): value.strip() for
            key, value in
            (pair.split(':', 1)
             for pair in observation)}
