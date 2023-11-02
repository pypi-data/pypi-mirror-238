#!/bin/sh
latestversion=$(git tag | fgrep python-preserves@ | cut -d@ -f2 | sort -V -r | head -1)
(
    firstitem='y';
    printf '[';
    for version in $(ls ../../python/*/sitemap.xml | cut -d/ -f4 | grep -v 'latest' | grep -v 'dev' | sort -V -r)
    do
        if [ "$firstitem" = "y" ]
        then
            firstitem=n
        else
            printf ','
        fi
        if [ "$version" = "$latestversion" ]
        then
            aliases='["latest"]'
        else
            aliases='[]'
        fi
        printf '\n  {"version":"%s","title":"%s","aliases":%s}' "$version" "$version" "$aliases"
    done;
    printf '\n]'
) | tee ../../_data/python-versions.json
rm -f ../../python/latest
ln -s "$latestversion" ../../python/latest
