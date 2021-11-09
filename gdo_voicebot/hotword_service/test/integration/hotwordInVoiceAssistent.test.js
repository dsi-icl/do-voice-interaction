// const voiceAssistentService = require('../../../voice_assistant_service/src/routes/voice_assistant')
// import voiceAssistentService from '../../../voice_assistant_service/src/routes/voice_assistant'

jest.mock('../../src/routes/hotword.js', () => ({
    startListening: jest.fn().mockImplementation(() => 'Hotword startListening method called')
}))

test('Empty test', () => {
//    expect(sum(1, 2)).toBe(3);
})