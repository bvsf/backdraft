[For install Jenkins read this Source post](https://linuxize.com/post/how-to-install-jenkins-on-ubuntu-18-04/)

[For install Jenkins on Debian buster read this](https://linuxize.com/post/how-to-install-jenkins-on-debian-10/)

[For install OpenJDK on Debian read this](https://stackoverflow.com/questions/57031649/how-to-install-openjdk-8-jdk-on-debian-10-buster])

Resumen
- sudo apt-get update
- sudo apt-get install openjdk-8-jdk
- (for debian apt install gnupg)
- wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
- sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
- sudo apt-get update
- sudo apt-get install jenkins
- systemctl status jenkins
- go to http://localhost:8080
- sudo cat /var/lib/jenkins/secrets/initialAdminPassword
- copy the secret and paste it on jenkins page
- install suggested plugins
- create admin user
- confirm url
- done!
