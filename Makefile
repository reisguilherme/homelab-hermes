.PHONY: validate kustomize

validate:
	node scripts/validate.mjs

kustomize:
	kubectl kustomize kubernetes > /dev/null
