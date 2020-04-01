.PHONY: report
report:
	python scripts/make.py report
	git add README.md
	git commit -m "Update report"
	git push cord19 HEAD:master
	