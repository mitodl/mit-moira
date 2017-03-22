"""
Python client for accessing MIT's Moira_ system.
This client uses the SOAP_ API, which has a few unusual limitations, and
requires X.509 client certificates for access.

.. _Moira: http://kb.mit.edu/confluence/display/istcontrib/Moira+Overview
.. _SOAP: https://en.wikipedia.org/wiki/SOAP
"""

from zeep import Client, Transport

WSDL_URL = "https://ws-dev.mit.edu/moiraws/services/moira?wsdl"


class Moira(object):
    """
    The client that accesses Moira's SOAP API, powered by
    `zeep <http://docs.python-zeep.org>`_. Requires an X.509 certificate and
    private key.

    Args:
        cert_path (str): The path to an X.509 certificate file
        key_path (str): The path to an X.509 private key file
        proxy_id (str): Used in many API calls. Do not set this
            unless you know what you're doing.
    """
    def __init__(self, cert_path, key_path, proxy_id=""):
        transport = Transport()
        transport.session.cert = (cert_path, key_path)
        self.client = Client(WSDL_URL, transport=transport)
        # No idea what `proxy_id` is, but many actions in the API require one.
        self.proxy_id = proxy_id

    def user_memberships(self, username):
        """
        Look up all the lists that the user is a member of.

        Args:
            username (str): The MIT username of the user

        Returns:
            list of strings: names of the lists that this user is a member of.
        """
        return self.client.service.getUserLists(username, "USER", self.proxy_id)

    def list_attributes(self, name):
        """
        Look up the attributes of a list.

        Args:
            name (str): The name of the list

        Returns:
            dict: attributes of the list
        """
        result = self.client.service.getListAttributes(name, self.proxy_id)
        if isinstance(result, list) and len(result) == 1:
            return result[0]
        return result

    def list_exists(self, name):
        """
        Does this list exist?

        Args:
            name (str): The name of the list

        Returns:
            bool: whether the list exists
        """
        return bool(self.list_attributes(name))

    def add_member_to_list(self, username, listname, member_type="USER"):
        """
        Add a member to an existing list.

        Args:
            username (str): The username of the user to add
            listname (str): The name of the list to add the user to
            member_type (str): Normally, this should be "USER".
                If you are adding a list as a member of another list,
                set this to "LIST", instead.
        """
        return self.client.service.addMemberToList(
            listname, username, member_type, self.proxy_id
        )

    def create_list(
        self, name, description="Created by mit_moira library",
        is_active=True, is_public=True, is_hidden=True,
        is_group=False, is_nfs_group=False,
        is_mail_list=False, use_mailman=False, mailman_server=""
    ):
        """
        Create a new list.

        Args:
            name (str): The name of the new list
            description (str): A short description of this list
            is_active (bool): Should the new list be active?
                An inactive list cannot be used.
            is_public (bool): Should the new list be public?
                If a list is public, anyone may join without requesting
                permission. If not, the owners control entry to the list.
            is_hidden (bool): Should the new list be hidden?
                Presumably, a hidden list doesn't show up in search queries.
            is_group (bool): Something about AFS?
            is_nfs_group (bool): Presumably, create an
                `NFS group <https://en.wikipedia.org/wiki/Network_File_System>`_
                for this group? I don't actually know what this does.
            is_mail_list (bool): Presumably, create a mailing list.
            use_mailman (bool): Presumably, use
                `GNU Mailman <https://en.wikipedia.org/wiki/GNU_Mailman>`_
                to manage the mailing list.
            mailman_server (str): The Mailman server to use, if ``use_mailman``
                is True.
        """
        attrs = {
            "aceName": "mit_moira",
            "aceType": "LIST",
            "activeList": is_active,
            "description": description,
            "gid": "",
            "group": is_group,
            "hiddenList": is_hidden,
            "listName": name,
            "mailList": is_mail_list,
            "mailman": use_mailman,
            "mailmanServer": mailman_server,
            "memaceName": "mit_moira",
            "memaceType": "USER",
            "modby": "",
            "modtime": "",
            "modwith": "",
            "nfsgroup": is_nfs_group,
            "publicList": is_public,
        }
        return self.client.service.createList(attrs, self.proxy_id)

    def update_list(
        self, name, new_name=None, description="Updated by mit_moira library",
        is_active=True, is_public=True, is_hidden=True,
        is_group=False, is_nfs_group=False,
        is_mail_list=False, use_mailman=False, mailman_server=""
    ):
        """
        Update an existing list. Be warned that this will overwrite
        *all* attributes on the list, not just the ones you specify!

        Args:
            name (str): The name of the existing list to be updated
            new_name (str): If you wish to change the name of the list,
                set it here. Otherwise, the name will remain the same.
            description (str): A short description of this list
            is_active (bool): Should the list be active?
                An inactive list cannot be used.
            is_public (bool): Should the list be public?
                If a list is public, anyone may join without requesting
                permission. If not, the owners control entry to the list.
            is_hidden (bool): Should the list be hidden?
                Presumably, a hidden list doesn't show up in search queries.
            is_group (bool): Something about AFS?
            is_nfs_group (bool): Presumably, have an
                `NFS group <https://en.wikipedia.org/wiki/Network_File_System>`_
                for this group? I don't actually know what this does.
            is_mail_list (bool): Presumably, have a mailing list.
            use_mailman (bool): Presumably, have
                `GNU Mailman <https://en.wikipedia.org/wiki/GNU_Mailman>`_
                manage the mailing list.
            mailman_server (str): The Mailman server to use, if ``use_mailman``
                is True.
        """
        attrs = {
            "aceName": "mit_moira",
            "aceType": "LIST",
            "activeList": is_active,
            "description": description,
            "gid": "",
            "group": is_group,
            "hiddenList": is_hidden,
            "listName": new_name or name,
            "mailList": is_mail_list,
            "mailman": use_mailman,
            "mailmanServer": mailman_server,
            "memaceName": "mit_moira",
            "memaceType": "USER",
            "modby": "",
            "modtime": "",
            "modwith": "",
            "nfsgroup": is_nfs_group,
            "publicList": is_public,
        }
        return self.client.service.updateListAttributes(
            attrs, name, self.proxy_id
        )

    def print_capabilities(self):
        """
        Print out the capabilities of this SOAP API.
        """
        self.client.wsdl.dump()
