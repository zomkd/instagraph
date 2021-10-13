import { shallowMount, mount } from "@vue/test-utils"
import UserInfoTable from "../UserInfoTable.vue"
const fetch = require("node-fetch");
jest.mock('node-fetch');

describe('UserInfoTable.vue', () => {
    it('mocks module to union graph', () => {
        const wrapper = shallowMount(UserInfoTable, { stubs: ['router-link'], 
        propsData: { userData: [{ id: '1', username: "tema_ok" }] } });
        wrapper.find('#union-graph-but').trigger('click')

        expect(fetch).toHaveBeenCalledTimes(1);
        expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/user_union_graph/', {
            method: "post",
            headers: {
                "Content-Type": "application/json",
            },
            body: "{\"graphsQueue\":[]}",
        });
    });
});

describe('UserInfoTable.vue', () => {
    it('test varible isComponentVisible', async () => {
        const wrapper = shallowMount(UserInfoTable, { stubs: ['router-link'], 
        propsData: { userData: [{ id: '1', username: "tema_ok" }] } });
        await wrapper.setData({ isComponentVisible: true })

        expect(wrapper.vm.isComponentVisible).toBe(true)
    });
});


describe('UserInfoTable.vue', () => {
    it('test varible isQueueVisible', async () => {
        const wrapper = shallowMount(UserInfoTable, { stubs: ['router-link'], 
        propsData: { userData: [{ id: '1', username: "tema_ok" }] } });
        await wrapper.setData({ isQueueVisible: true })

        expect(wrapper.vm.isQueueVisible).toBe(true)
    });
});


describe('UserInfoTable.vue', () => {
    it('test varible filterField', async () => {
        const wrapper = shallowMount(UserInfoTable, { stubs: ['router-link'], 
        propsData: { userData: [{ id: '1', username: "tema_ok" }] } });
        await wrapper.setData({ filterField: "asd" })

        expect(wrapper.vm.filterField).toBe("asd")
    });
});


describe('UserInfoTable.vue', () => {
    it('test varible selectedComponent', async () => {
        const wrapper = shallowMount(UserInfoTable, { stubs: ['router-link'], 
        propsData: { userData: [{ id: '1', username: "tema_ok" }] } });
        await wrapper.setData({ selectedComponent: "check", })

        expect(wrapper.vm.selectedComponent).toBe("check")
    });
});


describe('UserInfoTable.vue', () => {
    it('test varible currentSortDir', async () => {
        const wrapper = shallowMount(UserInfoTable, { stubs: ['router-link'], 
        propsData: { userData: [{ id: '1', username: "tema_ok" }] } });
        await wrapper.setData({ currentSortDir: "check", })

        expect(wrapper.vm.currentSortDir).toBe("check")
    });
});
