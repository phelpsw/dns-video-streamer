## DNS Video Streamer

Embed a video (or generic file) in TXT records in a DNS zone file.  Also
provides a downloader to retrieve the content.

### Setup

#### Encode / Zone
```
python binder.py vid.mp4 out.com
```

#### Server
Assuming ubuntu 16.04 installation.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install bind9
```

Add the following to `/etc/bind/named.conf.local`:
```
zone "movies.zzyzxgazette.xyz" {
    type master;
    file "/etc/bind/db.movies.zzyzxgazette.xyz"; # zone file path
};
```

Copy the output of the zone generator to the bind instance
```
scp -i ~/.ssh/aws.pem ~/projects/dnsvideo/out.com ubuntu@host:~/
```

Move configuration into place and set permissions
```
sudo mv ~/out.com /etc/bind/db.movies.zzyzxgazette.xyz
sudo chown root:root /etc/bind/db.movies.zzyzxgazette.xyz
sudo chmod 644 /etc/bind/db.movies.zzyzxgazette.xyz
sudo systemctl restart bind9.service
```




#### TODO:
 * Parallelize requests to facilitate streaming
