import React from "react";
import {Link} from "react-router-dom";

const EmployeeTableRow = function (props) {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  });
  return (
    <tr>
      <td>{props.name}</td>
      <td>{props.department}</td>
      <td className="has-text-right">{ formatter.format(props.salary) }</td>
      <td className="has-text-right">
        <Link to={`/edit/${props.id}`}>
          <span>Edit</span>
        </Link>
        <a style={{'marginLeft': '1em'}} onClick={() => props.delete(props.index)}>
          <span>Delete</span>
        </a>
      </td>
    </tr>
  );
}

export default EmployeeTableRow;
