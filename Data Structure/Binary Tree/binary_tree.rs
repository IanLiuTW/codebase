// Building a binary tree in Rust
#[derive(Debug, PartialEq, Eq)]
pub struct TreeNode {
    pub val: i32,
    pub left: Option<Rc<RefCell<TreeNode>>>,
    pub right: Option<Rc<RefCell<TreeNode>>>,
}

impl TreeNode {
    #[inline]
    pub fn new(val: i32) -> Self {
        TreeNode {
            val,
            left: None,
            right: None,
        }
    }
}

// Example to manipulate a binary tree
use std::cell::RefCell;
use std::rc::Rc;
impl Solution {
    pub fn min_depth(root: Option<Rc<RefCell<TreeNode>>>) -> i32 {
        if root.is_none() {
            return 0;
        }
        let mut depth = 1;
        let mut current_layer = vec![root];
        let mut next_layer: Vec<Option<Rc<_>>> = vec![];
        while !current_layer.is_empty() {
            for node in current_layer {
                if let Some(node) = node {
                    if node.borrow().left.is_none() && node.borrow().right.is_none() {
                        return depth;
                    }
                    if let Some(left) = &node.borrow().left {
                        next_layer.push(Some(Rc::clone(&left)));
                    }
                    if let Some(right) = &node.borrow().right {
                        next_layer.push(Some(Rc::clone(&right)));
                    }
                }
            }
            current_layer = next_layer;
            next_layer = vec![];
            depth += 1;
        }
        depth
    }
}
