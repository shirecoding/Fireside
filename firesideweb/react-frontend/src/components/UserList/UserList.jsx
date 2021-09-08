import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { FixedSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100%",
    width: "100%",
    backgroundColor: theme.palette.background.paper,
  },
}));

const renderRow = (props) => {
  const { data, index, style } = props;
  return (
    <ListItem button style={style} key={index}>
      <ListItemText secondary={data[index].name} />
    </ListItem>
  );
};

const UserList = ({ users }) => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AutoSizer>
        {({ height, width }) => (
          <FixedSizeList
            height={height}
            width={width}
            itemSize={22}
            itemCount={users.length}
            itemData={users}
          >
            {renderRow}
          </FixedSizeList>
        )}
      </AutoSizer>
    </div>
  );
};

export default UserList;
