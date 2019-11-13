import React, { Component } from "react";
import DatabaseTable from "../tables/DatabaseTable";
import GetModuleMarkButton from "../buttons/GetModuleDataButton";

type ModuleMark = {
  courseCode: string;
  student: string;
  alphanum: string;
};

class GetModuleMarkUnit extends Component {
  state = {
    data: []
  };

  componentDidMount() {
    this.setState({ data: [] });
  }

  getDataHandler = (moduleData: ModuleMark[]) => {
    console.log("Returned Data: " + moduleData);
    this.setState({ data: moduleData });
  };

  render() {
    console.log("Rendering ModuleMarkUnit");
    console.log("State: " + this.state.data);

    return (
      <div className="col-md-6 mx-auto">
        <GetModuleMarkButton returnData={this.getDataHandler.bind(this)} />
        <DatabaseTable data={this.state.data} />
      </div>
    );
  }
}
export default GetModuleMarkUnit;