"""GraphQL queries."""

DATA = """query data($id: ID!) { data(id: $id) {
    id filename filetype size category created isDirectory isBinary private
    upstreamProcessExecution { id processName execution {
        id pipelineVersion { id pipeline { id name } }
    } }
    annotationLane { id name } multiplexedLane { id name }
    sample { id name } project { id name } owner { id username name }
    multiplexedLane { id name }
    genome { id name organism { name } }
    genomeFasta { id name organism { name } }
    genomeGtf { id name organism { name } }
} }"""


SAMPLE = """query sample($id: ID!) {
    sample(id: $id) {
        id name private created category owner { id name username }
        initialData { id created data { id filename } } organism { id name }
        source { id name } purificationTarget { id name } project { id name }
        sourceText purificationTargetText threePrimeAdapterName
        scientist pi organisation purificationAgent experimentalMethod condition
        sequencer comments fivePrimeBarcodeSequence threePrimeBarcodeSequence 
        threePrimeAdapterSequence read1Primer read2Primer rtPrimer
        umiBarcodeSequence umiSeparator strandedness rnaSelectionMethod
        geo ena pubmed
    }
}"""


LANE = """query lane($id: ID!) { lane(id: $id) {
    id name private created owner { id name username }
    multiplexed { id filename } annotations { id filename }
} }"""


PIPELINE = """{ pipelineCategories {
    subcategories { pipelines { name version { id name } } } 
} }"""

EXECUTION = """query execution($id: ID!) { execution(id: $id) {
    id pipelineVersion { id name description schema pipeline { id name } }
    nextflowVersion forcedPublicProjectId forcedPublicSampleId canEdit canShare
    created started finished taskStarted taskFinished identifier private hasReport
    params dataParams sampleParams stdout stderr status dependent command log
    upstreamData { id filename } owner { id name username }
    upstreamSamples { id name } genome { id name organism { id name } }
    sample { id name } project { id name }
    processExecutions {
        id identifier name processName started finished stdout stderr bash status exitCode
        upstreamData { id filename } upstreamSamples { id name }
        downstreamData { id filename filetype size created owner { name } isRemoved }
    }
} }"""