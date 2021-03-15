#!/bin/sh
echo "[ check perl code ]"
for i in $(find .. -type f \( -name "*.pl" -o -name "*.pm" \)); do
    if head -1 "${i}" | grep ' \-T' >/dev/null; then
        if ! perl -T -c "${i}"; then
            echo "SYNTAX ERROR: ${i}"
	    exit 1
        fi
    else 
        if ! perl -c "${i}"; then
            echo "SYNTAX ERROR: ${i}"
	    exit 1
        fi
    fi
done

echo "[ check python code ]"
find .. -name "*.py" -exec python -m py_compile "{}" \;

echo "[ check javascript code ]"
for i in $(find .. -name "*.js"); do
    if ! node -c "${i}"; then
        echo "SYNTAX ERROR: ${i}"
        exit 1
    fi
done

echo "[ check yaml syntax ]"
for i in $(find .. -name "*.yml"); do
    if [ "${i}" == "../files/ansible/inventory.yml" ]; then
        continue
    fi
    if ! perl -MYAML -e "use YAML;YAML::LoadFile('${i}')"; then
        echo "SYNTAX ERROR: ${i}"
        exit 1
    fi
done

echo "[ check bash syntax ]"
for i in $(find .. -name "*.sh"); do
    if ! bash -n "${i}"; then
        echo "SYNTAX ERROR: ${i}"
        exit 1
    fi
done

echo "[ check ansible syntax ]"
if ! ansible-lint ../files/ansible/inventory.yml; then
    echo "SYNTAX ERROR: ${i}"
    exit 1
fi
for i in ../files/ansible/playbooks/*; do
     if ! ansible-lint "${i}"; then
         echo "SYNTAX ERROR: ${i}"
         exit 1
     fi
done

echo "[ check html syntax ]"
for html_file in $(find .. -name "*.html"); do
    # skip auto generated code in docs
    if [[ "${html_file}" == *"docs"* ]]; then
      continue
    fi
    tidy_output=$(tidy -q -e "${html_file}" 3>&1 2>&1)
    if [ $? -eq 2 ];then
        echo "SYNTAX ERROR: ${html_file}"
        echo "${tidy_output}"
        exit 1
    fi
    echo "${html_file} syntax OK"
done

echo "[ done ]"
