Test the latest Docker with Vagrant
###################################
:date: 2017-09-15 10:57
:author: Gilles Lenfant
:tags: Vagrant, Docker, MacOS, Windows
:category: Blog
:slug: test-latest-docker-with-vagrant
:status: published
:summary: Play with the freshest Docker on MacOS or Windows

Want to experiment the latest Docker CE features on Linux when you have a MacOS or Windows box? Or just want to learn Docker in a sandbox?

Here is a simple ``Vagrantfile`` that will make your day. Just ``vagrant up`` (wait some minutes), then ``vagrant ssh`` and you're done.

Ah! There's a goodie: The file sharing is supported by NFS on MacOS and SMB on Windows. Both provide faster file sync than the default VBoxFS.

Comments, pull requests and any improvement suggestions are welcome.

[gist:id=7772f48aa17eb4e09d4a62390825eade]

Exits:

- `Docker <https://www.docker.com/>`_
- `Vagrant <https://www.vagrantup.com/>`_
- `VirtualBox <https://www.virtualbox.org/>`_
