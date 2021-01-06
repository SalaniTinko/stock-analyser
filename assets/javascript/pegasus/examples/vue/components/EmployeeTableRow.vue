<template>
  <tr>
    <td>{{ employee.name }}</td>
    <td>{{ employee.department }}</td>
    <td class="has-text-right">{{ formattedSalary }}</td>
    <td class="has-text-right">
      <a v-on:click="editEmployee">
        <span>Edit</span>
      </a>
      <a style="margin-left: 1em;" v-on:click="deleteEmployee">
        <span>Delete</span>
      </a>
    </td>
  </tr>
</template>

<script>

export default {
  name: 'EmployeeTableRow',
  props: {
    employee: Object,
    client: Object,
  },
  computed: {
    formattedSalary: function () {
      const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });
      return formatter.format(this.employee.salary);
    }
  },
  methods: {
    editEmployee: function () {
      this.$emit('edit-employee', this.employee);
    },
    deleteEmployee: function () {
      this.$emit('delete-employee', this.employee);
    },
  }
};
</script>

<style scoped>
</style>
