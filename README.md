# gmail2SMS
Un semplice polling imap su gmail, le mail interessate vengono estratte e mandate via sms attraverso il servizio Nexmo.
Il polling viene fatto con <a href="https://twistedmatrix.com/trac/">twisted</a> (che implementa il pattern reactor) e con l'aiuto di <a href="https://github.com/itamarst/crochet">crochet</a>.
