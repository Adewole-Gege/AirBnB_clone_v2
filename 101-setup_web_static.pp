# Puppet manifest to set up web servers for deployment
package { 'nginx':
  ensure => installed,
}

file { '/data/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
  recurse => true,
}

file { ['/data/web_static/', '/data/web_static/releases/', '/data/web_static/shared/', '/data/web_static/releases/test/']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>",
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0644',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

exec { 'update_nginx_config':
  command => "sed -i '/server_name _;/a \\ \\n    location /hbnb_static/ {\\n        alias /data/web_static/current/;\\n    }' /etc/nginx/sites-available/default && service nginx restart",
  require => Package['nginx'],
}
