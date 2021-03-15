function get_cookie {
    echo $(/bin/curl -s -I http://${ids_ip}:81/users/login | /bin/awk '/Set-Cookie:/{print $2}')
}
function get_csrf {
    echo $(/bin/curl -s http://${ids_ip}:81/users/login | /bin/awk -F'"' '/csrf-token/{print $2}')
}
function get_authtoken {
    echo $(/bin/curl -s http://${ids_ip}:81/users/login | /bin/awk -F'"' '/authenticity_token" type="hidden" value="/{print $(NF-1)}')
}
function get_user_session {
    ifs=
    authtoken=$(get_authtoken)
    csrf=$(get_csrf)
    login=$(/bin/curl -i -s 'http://${ids_ip}:81/users/login' -H "X-CSRF-Token: ${csrf}" --data "utf8=%E2%9C%93&authenticity_token=${authtoken}%3D&user%5Bemail%5D=snorby%40example.com&user%5Bpassword%5D=snorby&user%5Bremember_me%5D=0&user%5Bremember_me%5D=1")
    ses=$(echo ${login} | /bin/awk  /'Set-Cookie: _snorby_session=/{print $2}')
    user=$(echo ${login} | /bin/awk  /'Set-Cookie: remember_user_token=/{print $2}')
    echo "${user} ${ses}"
}
function get_dashboard {
    get_user_session=$(get_user_session)
    echo $(/bin/curl -s 'http://${ids_ip}:81/' -H "X-CSRF-Token: ${csrf}" -H "Cookie: $(get_user_session)")
}
