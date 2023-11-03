import unittest
from zeroconf import Zeroconf
from unittest.mock import Mock, patch, MagicMock
from SBKodiak.KodiakMDNsLocate import find_kodiak_ip_addresses, MyListener


class TestFindKodiakIPAddresses(unittest.TestCase):

    # Pathcing the import of KodiakGlobals
    @patch('SBKodiak.KodiakGlobals.KodiakGlobals')
    def test_find_kodiak_ip_addresses(self, mock_kodiak_mdns_locator):
        # Create a mock listenerself
        listener = MyListener()

        # Mock the zero conf class and its behavior
        mock_zeroconf_instance = Mock()
        mock_zeroconf_instance.register_service = Mock()
        mock_zeroconf_instance.unregister_service = Mock()
        mock_zeroconf_instance.services = {1: "ServiceInfo"}

        # patchng the time.sleep import
        with patch("time.sleep"):
            # Patching the listener import as the new listenner just created
            with patch("SBKodiak.KodiakMDNsLocate.MyListener", return_value=listener):
                ip_addresses = find_kodiak_ip_addresses()

        self.assertEqual(ip_addresses, listener.found_ip_addresses)

    def test_add_service(self):
        listener = MyListener()
        zeroconf = MagicMock()
        info = MagicMock()
        info.addresses = [b'\xc0\xa8\x01\x01']  # IP address 192.168.1.1
        zeroconf.get_service_info.return_value = info

        listener.add_service(zeroconf, "_kodiak._tcp.local.", "KodiakService")
        self.assertEqual(listener.found_ip_addresses, ["192.168.1.1"])

    def test_update_service(self):
        listener = MyListener()
        listener.update_service()

if __name__ == '__main__':
    unittest.main()
