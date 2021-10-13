import { shallowMount, mount } from "@vue/test-utils"
import UsernameForm from "../UsernameForm.vue"
const fetch = require("node-fetch");
jest.mock('node-fetch');

describe('UsernameForm.vue', () => {
    it('mocks module',  () => {
        const wrapper = shallowMount(UsernameForm, { stubs: ['router-link'] });
        wrapper.find('#search-button').trigger('click')

        expect(fetch).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/username/', {
            method: "post",
            headers: {
                "Content-Type": "application/json",
            },
            body: "{\"username\":[\"\"]}",
        });
    });
});