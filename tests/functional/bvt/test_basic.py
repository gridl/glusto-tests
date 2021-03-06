#  Copyright (C) 2015-2016  Red Hat, Inc. <http://www.redhat.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

""" Description: BVT-Basic Tests """

import pytest
import time
from glusto.core import Glusto as g
from glustolibs.gluster.gluster_base_class import GlusterBaseClass
from glustolibs.gluster.exceptions import ExecutionError
from glustolibs.gluster.gluster_init import (
    is_glusterd_running, restart_glusterd, start_glusterd, stop_glusterd)


class TestGlusterdSanity(GlusterBaseClass):
    """GLusterd Sanity check
    """
    def setUp(self):
        """setUp required for tests
        """
        # Calling GlusterBaseClass setUp
        GlusterBaseClass.setUp.im_func(self)

        # Defining this variable to check if restart glusterd is required
        # in teardown
        self.test_method_complete = False

    @pytest.mark.bvt_basic
    def test_glusterd_restart_stop_start(self):
        """Tests glusterd stop, start, restart and validate if all
        peers are in connected state after glusterd restarts.
        """
        # restart glusterd on all servers
        g.log.info("Restart glusterd on all servers %s", self.servers)
        ret = restart_glusterd(self.servers)
        self.assertTrue(ret, ("Failed to restart glusterd on all servers %s",
                              self.servers))
        g.log.info("Successfully restarted glusterd on all servers %s",
                   self.servers)

        # Check if glusterd is running on all servers(expected: active)
        g.log.info("Check if glusterd is running on all servers %s"
                   "(expected: active)", self.servers)
        ret = is_glusterd_running(self.servers)
        self.assertEqual(ret, 0, ("Glusterd is not running on all servers %s",
                                  self.servers))
        g.log.info("Glusterd is running on all the servers %s", self.servers)

        # Stop glusterd on all servers
        g.log.info("Stop glusterd on all servers %s", self.servers)
        ret = stop_glusterd(self.servers)
        self.assertTrue(ret, ("Failed to stop glusterd on all servers %s",
                              self.servers))
        g.log.info("Successfully stopped glusterd on all servers %s",
                   self.servers)

        # Check if glusterd is running on all servers(expected: not running)
        g.log.info("Check if glusterd is running on all servers %s"
                   "(expected: not running)", self.servers)
        ret = is_glusterd_running(self.servers)
        self.assertNotEqual(ret, 0, ("Glusterd is still running on some "
                                     "servers %s", self.servers))
        g.log.info("Glusterd not running on any servers %s as expected.",
                   self.servers)

        # Start glusterd on all servers
        g.log.info("Start glusterd on all servers %s", self.servers)
        ret = start_glusterd(self.servers)
        self.assertTrue(ret, ("Failed to start glusterd on all servers %s",
                              self.servers))
        g.log.info("Successfully started glusterd on all servers %s",
                   self.servers)

        # Check if glusterd is running on all servers(expected: active)
        g.log.info("Check if glusterd is running on all servers %s"
                   "(expected: active)", self.servers)
        ret = is_glusterd_running(self.servers)
        self.assertEqual(ret, 0, ("Glusterd is not running on all servers %s",
                                  self.servers))
        g.log.info("Glusterd is running on all the servers %s", self.servers)

        # Wait for all the glusterd's to establish communication.
        time.sleep(30)

        # Validate all the peers are in connected state
        g.log.info("Validating all the peers are in Cluster and Connected")
        ret = self.validate_peers_are_connected()
        self.assertTrue(ret, "Validating Peers to be in Cluster Failed")
        g.log.info("All peers are in connected state")

        self.test_method_complete = True

    def tearDown(self):
        """In case of any failure restart glusterd on all servers
        """
        if not self.test_method_complete:
            # restart glusterd on all servers
            g.log.info("Restart glusterd on all servers %s", self.servers)
            ret = restart_glusterd(self.servers)
            if not ret:
                raise ExecutionError("Failed to restart glusterd on all "
                                     "servers %s", self.servers)
            g.log.info("Successfully restarted glusterd on all servers %s",
                       self.servers)

            # Wait for all the glusterd's to establish communication.
            time.sleep(30)

            # Validate all the peers are in connected state
            g.log.info("Validating all the peers are in Cluster and Connected")
            ret = self.validate_peers_are_connected()
            if not ret:
                raise ExecutionError("Validating Peers to be in Cluster "
                                     "Failed")
            g.log.info("All peers are in connected state")

        # Calling GlusterBaseClass tearDown
        GlusterBaseClass.tearDown.im_func(self)
