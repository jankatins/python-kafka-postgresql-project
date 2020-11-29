
setup-infra-aiven: aiven.env setup-local
	# This assumes the current default project is used and that's updated to use the correct cloud
	# avn project create <project-name>
	# avn project switch <project-name>
	# avn project update --cloud do-fra
	# yes `- <command>` is bad, but seems to be the easiest way without starting parsing service lists
	# no hobbyist plan available?
	-avn service create --plan startup-2 checkweb-kafka -t kafka || true
	-avn service topic-create checkweb-kafka checkweb --partitions 1 --replication 2 || true
	-avn service update checkweb-kafka -c kafka.auto_create_topics_enable=true
	-avn service create --plan hobbyist checkweb-postgres -t pg || true
	avn service user-creds-download checkweb-kafka --username avnadmin
	make list-aiven-infra

aiven.env:
	cat local.env.example | sed "s#KAFKA_CERT_PATH=#KAFKA_CERT_PATH=$(CURDIR)#" >> aiven.env
	echo "Please adjust the aiven.env file!"
