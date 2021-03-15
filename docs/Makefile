#
#
DEPENDENCIES="pandoc texlive"
ifdef DISTRO
	PANDOC_ARGS:="-Vlof --top-level-division=chapter --table-of-contents"
else
	PANDOC_ARGS:="-Vlof -V lang=swedish --chapters --table-of-contents"
endif

#depend:
#	sudo yum install $(DEPENDENCIES)

all: 96_refs.md pdf html epub docx

clean:
	@for i in bok.html bok.pdf bok.epub bok.docx; do \
		if [ -f $$i ];then \
			rm $$i; \
		fi \
	done
	@if [ -f 96_refs.md ];then \
		rm -f 96_refs.md; \
	fi

96_refs.md: 95_refs.md
	./scripts/gen_refs.pl

epub: 96_refs.md *.md
	pandoc *.md -o bok.epub ${PANDOC_ARGS}
# Should we have stylesheet on epub?
#--epub-stylesheet css/style.css

docx: 96_refs.md *.md
	pandoc *.md -o bok.docx ${PANDOC_ARGS}

pdf: 96_refs.md *.md
	pandoc *.md -o bok.pdf ${PANDOC_ARGS} --template=default.latex

html: 96_refs.md *.md
	pandoc *.md -o bok.html -c css/style.css --table-of-contents -w html5 -Vlof
	@sed -i.tmp '/googlecode.com/c\'$$'\n''<link rel=stylesheet href=css/ie9html5.js>\n' bok.html
	@rm bok.html.tmp
	@sed -i.tmp s/\ style=\"text-align\:\ left\;\"\//g bok.html
	@rm bok.html.tmp
	@sed -i.tmp 's/<col .*<thead>/<thead>/g' bok.html
	@rm bok.html.tmp
