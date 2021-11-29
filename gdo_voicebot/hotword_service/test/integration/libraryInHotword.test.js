const WakewordDetector = require('@mathquis/node-personal-wakeword')
const hotwordService = require('../../src/routes/hotword')
const path = require('path')
const Response = require('response')

jest.setTimeout(10000)

jest.mock('@mathquis/node-personal-wakeword') 

beforeEach(async () => {
    // Clear all instances and calls to constructor and all methods:
    // WakewordDetector.mockClear()

    const audioFile = path.resolve(__dirname, '../../keywords', './heyGalileo1.wav')

    let res = new Response(null, {
        status: 100,
        statusText: "",
        headers: {
        'Content-type': 'application/json'
        }
    })

    const req = {
        method: 'post',
        headers: { 'Content-type': 'text/plain' },
        body: audioFile
    }

    await hotwordService.setUpKeywordClient(true)
    await hotwordService.startListening(req, res, true)
})

test('Library object is created successfully', async () => {
    expect(WakewordDetector).toHaveBeenCalledTimes(1)
})

test('"Hey Galileo" hotword added', async () => {
    const mockWakewordDetectorInstance = WakewordDetector.mock.instances[0]
    const mockAddKeyword = mockWakewordDetectorInstance.addKeyword
    // expect(mockAddKeyword).toHaveBeenCalledWith() -- check arguments here
    expect(mockAddKeyword).toHaveBeenCalledTimes(2)
})

test('"Hey Galileo" hotword enabled', async () => {
    const mockWakewordDetectorInstance = WakewordDetector.mock.instances[0]
    const mockEnableKeyword = mockWakewordDetectorInstance.enableKeyword
    expect(mockEnableKeyword).toHaveBeenCalledWith('heyGalileo')
    expect(mockEnableKeyword).toHaveBeenCalledTimes(3)
})

test('Audio received is piped to library', async () => {
    const mockWakewordDetectorInstance = WakewordDetector.mock.instances[0]
    const mockPipe = mockWakewordDetectorInstance.pipe
    expect(mockPipe).toHaveBeenCalledTimes(1)
})